package main

import (
    "context"
    "flag"
    "fmt"
    "io"
    "log"
    "time"

    "google.golang.org/grpc"
    "google.golang.org/grpc/credentials/insecure"

    "lab05grpc/calculator"
)

func main() {
    serverAddr := flag.String(
        "server",
        "localhost:50051",
        "gRPC server address",
    )
    flag.Parse()

    conn, err := grpc.Dial(
        *serverAddr,
        grpc.WithTransportCredentials(insecure.NewCredentials()),
    )
    if err != nil {
        log.Fatalf("Failed to connect to server: %v", err)
    }
    defer conn.Close()

    client := calculator.NewCalculatorClient(conn)

    ctx, cancel := context.WithTimeout(
        context.Background(),
        10*time.Second,
    )
    defer cancel()

    fmt.Println("=== gRPC Calculator Client ===")
    fmt.Println()

    operations := []struct {
        name string
        a    float64
        b    float64
    }{
        {"add", 42, 18},
        {"subtract", 42, 18},
        {"multiply", 7, 6},
        {"divide", 42, 6},
        {"divide", 10, 0},
    }

    for _, op := range operations {
        resp, err := client.Calculate(ctx, &calculator.CalcRequest{
            Operation: op.name,
            A:         op.a,
            B:         op.b,
        })
        if err != nil {
            log.Printf("Calculation %s failed: %v", op.name, err)
            continue
        }

        if resp.Error != "" {
            fmt.Printf("%s(%.0f, %.0f): Error: %s\n",
                op.name, op.a, op.b, resp.Error)
        } else {
            fmt.Printf("%s(%.0f, %.0f) = %.2f\n",
                op.name, op.a, op.b, resp.Result)
        }
    }

    fmt.Println("\n--- Fibonacci Stream ---")

    stream, err := client.FibonacciStream(
        ctx,
        &calculator.FibRequest{Count: 10},
    )
    if err != nil {
        log.Fatalf("Failed to start Fibonacci stream: %v", err)
    }

    for {
        resp, err := stream.Recv()
        if err == io.EOF {
            fmt.Println("Fibonacci stream completed.")
            break
        }
        if err != nil {
            log.Fatalf("Failed to receive Fibonacci number: %v", err)
        }

        fmt.Printf("Fibonacci[%d] = %d\n", resp.Index, resp.Value)
    }
}
