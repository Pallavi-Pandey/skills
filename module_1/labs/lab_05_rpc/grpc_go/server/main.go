package main

import (
    "context"
    "fmt"
    "log"
    "net"

    "google.golang.org/grpc"

    "lab05grpc/calculator"
)

const port = ":50051"

type server struct {
    calculator.UnimplementedCalculatorServer
}

func (s *server) Calculate(
    ctx context.Context,
    req *calculator.CalcRequest,
) (*calculator.CalcResponse, error) {
    switch req.Operation {
    case "add":
        return &calculator.CalcResponse{
            Result: req.A + req.B,
        }, nil

    case "subtract":
        return &calculator.CalcResponse{
            Result: req.A - req.B,
        }, nil

    case "multiply":
        return &calculator.CalcResponse{
            Result: req.A * req.B,
        }, nil

    case "divide":
        if req.B == 0 {
            return &calculator.CalcResponse{
                Error: "division by zero",
            }, nil
        }
        return &calculator.CalcResponse{
            Result: req.A / req.B,
        }, nil

    default:
        return &calculator.CalcResponse{
            Error: "unknown operation",
        }, nil
    }
}

func (s *server) FibonacciStream(
    req *calculator.FibRequest,
    stream calculator.Calculator_FibonacciStreamServer,
) error {
    var a, b int64 = 0, 1

    for i := int32(0); i < req.Count; i++ {
        if err := stream.Send(&calculator.FibResponse{
            Value: a,
            Index: i,
        }); err != nil {
            return err
        }

        a, b = b, a+b
    }

    return nil
}

func main() {
    lis, err := net.Listen("tcp", port)
    if err != nil {
        log.Fatalf("failed to listen: %v", err)
    }

    grpcServer := grpc.NewServer()
    calculator.RegisterCalculatorServer(grpcServer, &server{})

    fmt.Printf("gRPC Calculator Server listening on %s\n", port)

    if err := grpcServer.Serve(lis); err != nil {
        log.Fatalf("failed to serve: %v", err)
    }
}
