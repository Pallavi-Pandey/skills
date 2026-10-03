// Lab 06 - URL Fetcher: Sequential vs Concurrent (SOLUTION)
package main

import (
	"fmt"
	"io"
	"net/http"
	"sync"
	"time"
)

var urls = []string{
	"https://httpbin.org/delay/1",
	"https://httpbin.org/get",
	"https://httpbin.org/ip",
	"https://httpbin.org/user-agent",
	"https://httpbin.org/headers",
	"https://httpbin.org/delay/1",
	"https://httpbin.org/get",
	"https://httpbin.org/ip",
	"https://httpbin.org/user-agent",
	"https://httpbin.org/headers",
	"https://httpbin.org/delay/1",
	"https://httpbin.org/get",
	"https://httpbin.org/ip",
	"https://httpbin.org/user-agent",
	"https://httpbin.org/headers",
	"https://httpbin.org/delay/1",
	"https://httpbin.org/get",
	"https://httpbin.org/ip",
	"https://httpbin.org/user-agent",
	"https://httpbin.org/headers",
}

func fetchURL(url string) (int, error) {
	resp, err := http.Get(url)
	if err != nil {
		return 0, err
	}
	defer resp.Body.Close()
	body, _ := io.ReadAll(resp.Body)
	return len(body), nil
}

func fetchSequential(urls []string) {
	fmt.Println("\n=== SEQUENTIAL FETCH ===")
	start := time.Now()

	for i, url := range urls {
		size, err := fetchURL(url)
		if err != nil {
			fmt.Printf("  [%d] ERROR: %s → %v\n", i, url, err)
		} else {
			fmt.Printf("  [%d] OK: %s → %d bytes\n", i, url, size)
		}
	}

	elapsed := time.Since(start)
	fmt.Printf("\nSequential: %d URLs in %v\n", len(urls), elapsed)
}

func fetchConcurrent(urls []string) {
	fmt.Println("\n=== CONCURRENT FETCH (goroutines) ===")
	start := time.Now()

	var wg sync.WaitGroup
	for i, url := range urls {
		wg.Add(1)
		go func(idx int, u string) {
			defer wg.Done()
			size, err := fetchURL(u)
			if err != nil {
				fmt.Printf("  [%d] ERROR: %s → %v\n", idx, u, err)
			} else {
				fmt.Printf("  [%d] OK: %s → %d bytes\n", idx, u, size)
			}
		}(i, url)
	}
	wg.Wait()

	elapsed := time.Since(start)
	fmt.Printf("\nConcurrent: %d URLs in %v\n", len(urls), elapsed)
}

func main() {
	fmt.Println("Lab 06: Sequential vs Concurrent URL Fetching")
	fmt.Printf("Fetching %d URLs...\n", len(urls))

	fetchSequential(urls)
	fetchConcurrent(urls)

	fmt.Println("\n--- COMPARISON ---")
	fmt.Println("Sequential fetches one at a time (slow)")
	fmt.Println("Concurrent fetches ALL at once (fast)")
	fmt.Println("Goroutines are ~2KB each vs ~1MB for OS threads!")
}
