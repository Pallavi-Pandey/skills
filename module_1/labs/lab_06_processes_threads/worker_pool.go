// Lab 06 - Worker Pool Pattern
package main

import (
    "flag"
    "fmt"
    "math/rand"
    "time"
)

type Job struct {
    ID       int
    Duration time.Duration
}

type Result struct {
    JobID    int
    WorkerID int
    Output   string
    Duration time.Duration
}

func worker(id int, jobs <-chan Job, results chan<- Result) {
    for job := range jobs {
        start := time.Now()
        time.Sleep(job.Duration)

        result := Result{
            JobID:    job.ID,
            WorkerID: id,
            Output:   fmt.Sprintf("Processed by worker %d", id),
            Duration: time.Since(start),
        }

        results <- result
        fmt.Printf("Worker %d completed job %d in %v\n",
            id, job.ID, result.Duration)
    }
}

func main() {
    numWorkers := flag.Int("workers", 3, "Number of workers")
    numJobs := flag.Int("jobs", 10, "Number of jobs")
    flag.Parse()

    if *numWorkers < 1 || *numJobs < 1 {
        fmt.Println("Error: workers and jobs must both be at least 1.")
        return
    }

    fmt.Printf("=== Worker Pool: %d workers, %d jobs ===\n\n",
        *numWorkers, *numJobs)

    jobs := make(chan Job, *numJobs)
    results := make(chan Result, *numJobs)

    for w := 1; w <= *numWorkers; w++ {
        go worker(w, jobs, results)
    }

    for j := 1; j <= *numJobs; j++ {
        duration := time.Duration(100+rand.Intn(400)) * time.Millisecond
        jobs <- Job{ID: j, Duration: duration}
    }
    close(jobs)

    for r := 1; r <= *numJobs; r++ {
        result := <-results
        fmt.Printf("Result: Job %d done by Worker %d in %v\n",
            result.JobID, result.WorkerID, result.Duration)
    }

    fmt.Println("\n--- KEY INSIGHTS ---")
    fmt.Println("1. Workers share a single jobs channel (fan-out)")
    fmt.Println("2. Results are collected in a single channel (fan-in)")
    fmt.Println("3. Go channels handle all the synchronization!")
}
