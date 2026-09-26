// Lab 06 - Worker Pool Pattern (Starter Code)
// =============================================
// Implements the fan-out/fan-in concurrency pattern.
// N workers process jobs from a shared channel.
//
// Fill in the TODOs.

package main

import (
	"flag"
	"fmt"
	"math/rand"
	"time"
)

// Job represents a unit of work
type Job struct {
	ID       int
	Duration time.Duration // Simulated work duration
}

// Result represents the output of processing a Job
type Result struct {
	JobID    int
	WorkerID int
	Output   string
	Duration time.Duration
}

func worker(id int, jobs <-chan Job, results chan<- Result) {
	// TODO: Loop over jobs channel (for job := range jobs)
	// TODO: For each job:
	//   1. Record the start time
	//   2. Simulate work with time.Sleep(job.Duration)
	//   3. Build a Result with the worker ID, job ID, and elapsed time
	//   4. Send the Result to the results channel
	//   5. Print a message like "Worker 3 completed job 7 in 250ms"

	// HINT:
	// for job := range jobs {
	//     start := time.Now()
	//     time.Sleep(job.Duration)
	//     results <- Result{
	//         JobID:    job.ID,
	//         WorkerID: id,
	//         Output:   fmt.Sprintf("Processed by worker %d", id),
	//         Duration: time.Since(start),
	//     }
	// }
}

func main() {
	numWorkers := flag.Int("workers", 3, "Number of workers")
	numJobs := flag.Int("jobs", 10, "Number of jobs")
	flag.Parse()

	fmt.Printf("=== Worker Pool: %d workers, %d jobs ===\n\n", *numWorkers, *numJobs)

	// TODO: Create a 'jobs' channel (buffered, capacity = numJobs)
	// TODO: Create a 'results' channel (buffered, capacity = numJobs)

	// TODO: Start worker goroutines
	// for w := 1; w <= *numWorkers; w++ {
	//     go worker(w, jobs, results)
	// }

	// TODO: Send jobs to the jobs channel
	// for j := 1; j <= *numJobs; j++ {
	//     duration := time.Duration(100+rand.Intn(400)) * time.Millisecond
	//     jobs <- Job{ID: j, Duration: duration}
	// }
	// close(jobs)  // Signal that no more jobs are coming

	// TODO: Collect results
	// for r := 1; r <= *numJobs; r++ {
	//     result := <-results
	//     fmt.Printf("  Result: Job %d done by Worker %d in %v\n", result.JobID, result.WorkerID, result.Duration)
	// }

	_ = rand.Intn // Remove when implemented

	fmt.Println("\n--- KEY INSIGHTS ---")
	fmt.Println("1. Workers share a single jobs channel (fan-out)")
	fmt.Println("2. Results are collected in a single channel (fan-in)")
	fmt.Println("3. Go channels handle all the synchronization!")
}
