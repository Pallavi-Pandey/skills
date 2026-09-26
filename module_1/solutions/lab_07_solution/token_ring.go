// Lab 07 - Token Ring (SOLUTION)
package main

import (
	"flag"
	"fmt"
	"math/rand"
	"sync"
	"time"
)

type Node struct {
	ID         int
	TotalNodes int
	HasToken   bool
	WantCS     bool
	InCS       bool
	NextChan   chan bool
	PrevChan   chan bool
}

func (n *Node) CriticalSection(csLog *[]string, mu *sync.Mutex) {
	n.InCS = true
	fmt.Printf("  [LOCK] [Node %d] ENTERING critical section\n", n.ID)
	work := time.Duration(100+rand.Intn(200)) * time.Millisecond
	time.Sleep(work)
	mu.Lock()
	*csLog = append(*csLog, fmt.Sprintf("Node %d (held for %v)", n.ID, work))
	mu.Unlock()
	fmt.Printf("  [UNLOCK] [Node %d] LEAVING critical section (worked for %v)\n", n.ID, work)
	n.InCS = false
}

func (n *Node) Run(wg *sync.WaitGroup, csLog *[]string, mu *sync.Mutex, rounds int) {
	defer wg.Done()
	csCount := 0

	for csCount < rounds {
		<-n.PrevChan
		fmt.Printf("  [MSG] [Node %d] Received token\n", n.ID)

		n.WantCS = rand.Float64() < 0.6

		if n.WantCS {
			n.CriticalSection(csLog, mu)
			csCount++
		} else {
			fmt.Printf("  [PASS] [Node %d] Do not need CS, passing token\n", n.ID)
		}

		n.NextChan <- true
		time.Sleep(50 * time.Millisecond)
	}
}

func main() {
	totalNodes := flag.Int("total", 4, "Number of nodes")
	rounds := flag.Int("rounds", 3, "CS entries per node")
	flag.Parse()

	fmt.Printf("=== Token Ring: %d nodes, %d rounds ===\n\n", *totalNodes, *rounds)

	channels := make([]chan bool, *totalNodes)
	for i := range channels {
		channels[i] = make(chan bool, 1)
	}

	nodes := make([]*Node, *totalNodes)
	for i := 0; i < *totalNodes; i++ {
		nodes[i] = &Node{
			ID:         i,
			TotalNodes: *totalNodes,
			PrevChan:   channels[i],
			NextChan:   channels[(i+1)%*totalNodes],
		}
	}

	var wg sync.WaitGroup
	var csLog []string
	var mu sync.Mutex

	for _, node := range nodes {
		wg.Add(1)
		go node.Run(&wg, &csLog, &mu, *rounds)
	}

	fmt.Println("[INIT] Injecting token at Node 0\n")
	channels[0] <- true

	wg.Wait()

	fmt.Println("\n=== Critical Section Log ===")
	for i, entry := range csLog {
		fmt.Printf("  %d. %s\n", i+1, entry)
	}
	fmt.Println("\n[OK] Mutual exclusion guaranteed by Token Ring algorithm")
}
