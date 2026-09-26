/**
 * Lab 08 - Deadlock Demo (Starter Code)
 * =======================================
 * Creates a classic deadlock: two threads, two locks, opposite order.
 *
 *   Thread 1: lock(A) → lock(B)
 *   Thread 2: lock(B) → lock(A)
 *
 * Fill in the TODOs to create the deadlock.
 */

public class DeadlockDemo {

    // Two shared resources (locks)
    private static final Object LOCK_A = new Object();
    private static final Object LOCK_B = new Object();

    // Shared bank accounts (the resource we're protecting)
    private static int accountA = 1000;
    private static int accountB = 1000;

    public static void main(String[] args) {
        System.out.println("=== Deadlock Demo ===");
        System.out.println("Account A: $" + accountA);
        System.out.println("Account B: $" + accountB);
        System.out.println("\nStarting two transfers simultaneously...\n");

        // Thread 1: Transfer $100 from A to B
        // Acquires LOCK_A first, then LOCK_B
        Thread transfer1 = new Thread(() -> {
            System.out.println("[T1] Trying to lock Account A...");

            // TODO: synchronized(LOCK_A) {
            //     System.out.println("[T1] Locked Account A [OK]");
            //     
            //     // Simulate some processing time (this makes the deadlock almost guaranteed)
            //     try { Thread.sleep(100); } catch (InterruptedException e) {}
            //     
            //     System.out.println("[T1] Trying to lock Account B...");
            //     synchronized(LOCK_B) {
            //         System.out.println("[T1] Locked Account B [OK]");
            //         accountA -= 100;
            //         accountB += 100;
            //         System.out.println("[T1] Transfer complete: A→B $100");
            //     }
            // }

        }, "Transfer-A-to-B");

        // Thread 2: Transfer $200 from B to A
        // Acquires LOCK_B first, then LOCK_A → OPPOSITE ORDER → DEADLOCK!
        Thread transfer2 = new Thread(() -> {
            System.out.println("[T2] Trying to lock Account B...");

            // TODO: synchronized(LOCK_B) {
            //     System.out.println("[T2] Locked Account B [OK]");
            //     
            //     try { Thread.sleep(100); } catch (InterruptedException e) {}
            //     
            //     System.out.println("[T2] Trying to lock Account A...");
            //     synchronized(LOCK_A) {
            //         System.out.println("[T2] Locked Account A [OK]");
            //         accountB -= 200;
            //         accountA += 200;
            //         System.out.println("[T2] Transfer complete: B→A $200");
            //     }
            // }

        }, "Transfer-B-to-A");

        transfer1.start();
        transfer2.start();

        // Wait a few seconds, then check if we're deadlocked
        try {
            transfer1.join(5000);
            transfer2.join(5000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        if (transfer1.isAlive() || transfer2.isAlive()) {
            System.out.println("\n[FATAL] DEADLOCK DETECTED!");
            System.out.println("Both threads are stuck waiting for each other.");
            System.out.println("\nRun 'jstack <pid>' from another terminal to see the deadlock.");
            System.out.println("Thread states:");
            System.out.println("  " + transfer1.getName() + ": " + transfer1.getState());
            System.out.println("  " + transfer2.getName() + ": " + transfer2.getState());

            // Build a wait-for graph
            System.out.println("\nWait-For Graph:");
            System.out.println("  T1 (holds A) → waits for B → held by T2");
            System.out.println("  T2 (holds B) → waits for A → held by T1");
            System.out.println("  CYCLE DETECTED → Deadlock!");

            // Force exit since threads are stuck
            System.exit(1);
        } else {
            System.out.println("\n[OK] Both transfers completed successfully (no deadlock occurred).");
            System.out.println("Account A: $" + accountA);
            System.out.println("Account B: $" + accountB);
        }
    }
}
