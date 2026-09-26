/**
 * Lab 08 - Deadlock Fixed (Starter Code)
 * ========================================
 * Two strategies to prevent deadlocks:
 *   1. Consistent lock ordering (always lock A before B)
 *   2. tryLock() with timeout (give up if you can't get the lock)
 *
 * Fill in the TODOs.
 */

import java.util.concurrent.locks.ReentrantLock;
import java.util.concurrent.TimeUnit;

public class DeadlockFixed {

    private static int accountA = 1000;
    private static int accountB = 1000;

    // ===== Strategy 1: Consistent Lock Ordering =====
    private static final Object LOCK_A = new Object();
    private static final Object LOCK_B = new Object();

    public static void fixedWithOrdering() {
        System.out.println("\n=== Fix 1: Consistent Lock Ordering ===");
        System.out.println("Rule: ALWAYS acquire LOCK_A before LOCK_B\n");

        Thread t1 = new Thread(() -> {
            // TODO: Both threads lock in the SAME order: A first, then B
            // synchronized(LOCK_A) {
            //     System.out.println("[T1] Locked A");
            //     try { Thread.sleep(100); } catch (InterruptedException e) {}
            //     synchronized(LOCK_B) {
            //         System.out.println("[T1] Locked B");
            //         accountA -= 100;
            //         accountB += 100;
            //         System.out.println("[T1] Transfer A→B $100 [OK]");
            //     }
            // }
        }, "Ordering-T1");

        Thread t2 = new Thread(() -> {
            // TODO: SAME order as T1! A first, then B (even though we're transferring B→A)
            // synchronized(LOCK_A) {   // ← Key difference! Was LOCK_B in the deadlock version
            //     System.out.println("[T2] Locked A");
            //     try { Thread.sleep(100); } catch (InterruptedException e) {}
            //     synchronized(LOCK_B) {
            //         System.out.println("[T2] Locked B");
            //         accountB -= 200;
            //         accountA += 200;
            //         System.out.println("[T2] Transfer B→A $200 [OK]");
            //     }
            // }
        }, "Ordering-T2");

        t1.start();
        t2.start();
        try { t1.join(); t2.join(); } catch (InterruptedException e) {}

        System.out.println("Balances: A=$" + accountA + " B=$" + accountB);
        System.out.println("[OK] No deadlock! Circular wait condition prevented.\n");
    }

    // ===== Strategy 2: tryLock with Timeout =====
    private static final ReentrantLock REENTRANT_A = new ReentrantLock();
    private static final ReentrantLock REENTRANT_B = new ReentrantLock();

    public static void fixedWithTryLock() {
        System.out.println("=== Fix 2: tryLock() with Timeout ===");
        System.out.println("Rule: If you can't get the lock in 1 second, give up and retry\n");

        // Reset accounts
        accountA = 1000;
        accountB = 1000;

        Thread t1 = new Thread(() -> {
            // TODO: Use tryLock with timeout
            // boolean success = false;
            // while (!success) {
            //     try {
            //         if (REENTRANT_A.tryLock(1, TimeUnit.SECONDS)) {
            //             try {
            //                 System.out.println("[T1] Locked A");
            //                 Thread.sleep(100);
            //                 if (REENTRANT_B.tryLock(1, TimeUnit.SECONDS)) {
            //                     try {
            //                         System.out.println("[T1] Locked B");
            //                         accountA -= 100;
            //                         accountB += 100;
            //                         System.out.println("[T1] Transfer A→B $100 [OK]");
            //                         success = true;
            //                     } finally {
            //                         REENTRANT_B.unlock();
            //                     }
            //                 } else {
            //                     System.out.println("[T1] Couldn't get B, releasing A and retrying...");
            //                 }
            //             } finally {
            //                 REENTRANT_A.unlock();
            //             }
            //         }
            //     } catch (InterruptedException e) {}
            // }
        }, "TryLock-T1");

        Thread t2 = new Thread(() -> {
            // TODO: Same pattern but with B first, then A
            // This would deadlock with synchronized, but tryLock backs off!
        }, "TryLock-T2");

        t1.start();
        t2.start();
        try { t1.join(); t2.join(); } catch (InterruptedException e) {}

        System.out.println("Balances: A=$" + accountA + " B=$" + accountB);
        System.out.println("[OK] No deadlock! tryLock() eliminates hold-and-wait / preemption issues.\n");
    }

    public static void main(String[] args) {
        System.out.println("=== Deadlock Prevention Strategies ===");
        fixedWithOrdering();
        fixedWithTryLock();

        System.out.println("--- Summary ---");
        System.out.println("Fix 1 (Lock Ordering): Breaks 'Circular Wait' condition");
        System.out.println("Fix 2 (tryLock):       Breaks 'No Preemption' condition");
        System.out.println("Both are used in production systems!");
    }
}
