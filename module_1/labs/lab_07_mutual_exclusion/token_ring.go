// Lab 07 - Token Ring Mutual Exclusion (Starter Code)
// =====================================================
// Simulates the Token Ring algorithm for distributed mutual exclusion.
// One token circulates around a ring of N nodes.
// Only the token holder can enter the critical section.
//
// This version simulates all nodes in one process using goroutines and channels.
//
// Fill in the TODOs.

package main

import (
	"flag"
	"fmt"
	"math/rand"
	"sync"
	"time"
)

// Node represents a process in the token ring
type Node struct {
	ID          int
	TotalNodes  int
	HasToken    bool
	WantCS      bool           // Does this node want to enter the critical section?
	InCS        bool           // Is this node currently in the critical section?
	NextChan    chan bool       // Channel to send token to next node
	PrevChan    chan bool       // Channel to receive token from previous node
}

// CriticalSection simulates doing work that requires mutual exclusion
func (n *Node) CriticalSection(csLog *[]string, mu *sync.Mutex) {
	n.InCS = true
	fmt.Printf("  [LOCK] [Node %d] ENTERING critical section\n", n.ID)
	
	// Simulate work
	work := time.Duration(100+rand.Intn(200)) * time.Millisecond
	time.Sleep(work)
	
	mu.Lock()
	*csLog = append(*csLog, fmt.Sprintf("Node %d (held for %v)", n.ID, work))
	mu.Unlock()
	
	fmt.Printf("  [UNLOCK] [Node %d] LEAVING critical section (worked for %v)\n", n.ID, work)
	n.InCS = false
}

// Run starts the node's main loop
func (n *Node) Run(wg *sync.WaitGroup, csLog *[]string, mu *sync.Mutex, rounds int) {
	defer wg.Done()
	
	csCount := 0

	for csCount < rounds {
		// TODO: Wait to receive the token from PrevChan
		// token := <-n.PrevChan
		
		// TODO: Now we have the token!
		// fmt.Printf("  [MSG] [Node %d] Received token\n", n.ID)

		// TODO: Decide if this node wants to enter the critical section
		// (simulate with random chance, e.g., 60% of the time)
		// n.WantCS = rand.Float64() < 0.6

		// TODO: If WantCS is true:
		//   1. Call n.CriticalSection(csLog, mu)
		//   2. Increment csCount
		// If not:
		//   fmt.Printf("  [PASS] [Node %d] Do not need CS, passing token\n", n.ID)

		// TODO: Pass the token to the next node
		// n.NextChan <- true

		// Small delay to make output readable
		time.Sleep(50 * time.Millisecond)
		
		// Remove this break when you implement the TODOs
		break
	}
}

func main() {
	totalNodes := flag.Int("total", 4, "Number of nodes in the ring")
	rounds := flag.Int("rounds", 3, "CS entries per node before stopping")
	flag.Parse()

	fmt.Printf("=== Token Ring Mutual Exclusion ===\n")
	fmt.Printf("Nodes: %d | Rounds per node: %d\n\n", *totalNodes, *rounds)

	// Create channels for the ring
	channels := make([]chan bool, *totalNodes)
	for i := range channels {
		channels[i] = make(chan bool, 1) // Buffered so token can be placed
	}

	// Create nodes
	nodes := make([]*Node, *totalNodes)
	for i := 0; i < *totalNodes; i++ {
		nodes[i] = &Node{
			ID:         i,
			TotalNodes: *totalNodes,
			PrevChan:   channels[i],                       // Receive from this channel
			NextChan:   channels[(i+1)%*totalNodes],       // Send to next node's channel
		}
	}

	// Start all nodes
	var wg sync.WaitGroup
	var csLog []string
	var mu sync.Mutex

	for _, node := range nodes {
		wg.Add(1)
		go node.Run(&wg, &csLog, &mu, *rounds)
	}

	// Inject the token at Node 0
	fmt.Println("[INIT] Injecting token at Node 0\n")
	channels[0] <- true

	wg.Wait()

	// Print summary
	fmt.Println("\n=== Critical Section Log ===")
	for i, entry := range csLog {
		fmt.Printf("  %d. %s\n", i+1, entry)
	}
	fmt.Println("\n[OK] No two nodes were in the CS simultaneously (Token Ring guarantees this)")
}
