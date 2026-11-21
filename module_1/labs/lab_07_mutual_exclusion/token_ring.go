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

func (n *Node) Run(
    wg *sync.WaitGroup,
    csLog *[]string,
    mu *sync.Mutex,
    rounds int,
    done []bool,
    stateMu *sync.Mutex,
) {
    defer wg.Done()
    csCount := 0

    for {
        // Wait until the previous node passes the token.
        <-n.PrevChan
        n.HasToken = true
        fmt.Printf("  [MSG] [Node %d] Received token\n", n.ID)

        if csCount < rounds {
            n.WantCS = rand.Float64() < 0.6

            if n.WantCS {
                n.CriticalSection(csLog, mu)
                csCount++

                if csCount == rounds {
                    stateMu.Lock()
                    done[n.ID] = true
                    stateMu.Unlock()
                    fmt.Printf("  [DONE] [Node %d] Completed all %d rounds\n", n.ID, rounds)
                }
            } else {
                fmt.Printf("  [PASS] [Node %d] Does not need the critical section\n", n.ID)
            }
        } else {
            fmt.Printf("  [PASS] [Node %d] Already completed its rounds\n", n.ID)
        }

        // Check whether every node has finished.
        stateMu.Lock()
        allDone := true
        for _, finished := range done {
            if !finished {
                allDone = false
                break
            }
        }
        stateMu.Unlock()

        n.HasToken = false

        // The final node to finish can stop the ring.
        if allDone {
                fmt.Println("[INFO] All nodes completed their rounds.")
                n.NextChan <- true
                return
        }

        // Always pass the token, even when this node did no work.
        n.NextChan <- true
        time.Sleep(50 * time.Millisecond)
    }
}

func main() {
    totalNodes := flag.Int("total", 4, "Number of nodes in the ring")
    rounds := flag.Int("rounds", 3, "Critical-section entries per node")
    flag.Parse()

    if *totalNodes < 1 || *rounds < 1 {
        fmt.Println("Error: total nodes and rounds must both be at least 1.")
        return
    }

    fmt.Println("=== Token Ring Mutual Exclusion ===")
    fmt.Printf("Nodes: %d | Rounds per node: %d\n\n", *totalNodes, *rounds)

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
    done := make([]bool, *totalNodes)
    var stateMu sync.Mutex

    for _, node := range nodes {
        wg.Add(1)
        go node.Run(&wg, &csLog, &mu, *rounds, done, &stateMu)
    }

    fmt.Println("[INIT] Injecting token at Node 0\n")
    channels[0] <- true

    wg.Wait()

    fmt.Println("\n=== Critical Section Log ===")
    for i, entry := range csLog {
        fmt.Printf("  %d. %s\n", i+1, entry)
    }

    fmt.Printf("\n[OK] All %d nodes completed %d critical-section entries each.\n",
        *totalNodes, *rounds)
}
