// Lab 06 - Worker Pool (SOLUTION)
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
		elapsed := time.Since(start)
		results <- Result{
			JobID:    job.ID,
			WorkerID: id,
			Output:   fmt.Sprintf("Processed by worker %d", id),
			Duration: elapsed,
		}
		fmt.Printf("  Worker %d completed job %d in %v\n", id, job.ID, elapsed)
	}
}

func main() {
	numWorkers := flag.Int("workers", 3, "Number of workers")
	numJobs := flag.Int("jobs", 10, "Number of jobs")
	flag.Parse()

	fmt.Printf("=== Worker Pool: %d workers, %d jobs ===\n\n", *numWorkers, *numJobs)
	start := time.Now()

	jobs := make(chan Job, *numJobs)
	results := make(chan Result, *numJobs)

	for w := 1; w <= *numWorkers; w++ {
		go worker(w, jobs, results)
	}

	totalWork := time.Duration(0)
	for j := 1; j <= *numJobs; j++ {
		d := time.Duration(100+rand.Intn(400)) * time.Millisecond
		totalWork += d
		jobs <- Job{ID: j, Duration: d}
	}
	close(jobs)

	for r := 1; r <= *numJobs; r++ {
		<-results
	}

	elapsed := time.Since(start)
	fmt.Printf("\nTotal wall time:   %v\n", elapsed)
	fmt.Printf("Total work time:   %v\n", totalWork)
	fmt.Printf("Speedup:           %.1fx\n", float64(totalWork)/float64(elapsed))
}
