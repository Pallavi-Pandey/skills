/**
 * Lab 08 - Deadlock Fixed
 * Strategy 1: Consistent lock ordering
 * Strategy 2: tryLock with timeout
 */

import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.ReentrantLock;

public class DeadlockFixed {

    private static int accountA = 1000;
    private static int accountB = 1000;

    private static final Object LOCK_A = new Object();
    private static final Object LOCK_B = new Object();

    public static void fixedWithOrdering() {
        System.out.println("\n=== Fix 1: Consistent Lock Ordering ===");
        System.out.println("Rule: Always acquire A before B\n");

        accountA = 1000;
        accountB = 1000;

        Thread t1 = new Thread(() -> {
            synchronized (LOCK_A) {
                System.out.println("[T1] Locked A");
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    return;
                }

                synchronized (LOCK_B) {
                    System.out.println("[T1] Locked B");
                    accountA -= 100;
                    accountB += 100;
                    System.out.println("[T1] Transfer A to B: $100 [OK]");
                }
            }
        }, "Ordering-T1");

        Thread t2 = new Thread(() -> {
            synchronized (LOCK_A) {
                System.out.println("[T2] Locked A");
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    return;
                }

                synchronized (LOCK_B) {
                    System.out.println("[T2] Locked B");
                    accountB -= 200;
                    accountA += 200;
                    System.out.println("[T2] Transfer B to A: $200 [OK]");
                }
            }
        }, "Ordering-T2");

        t1.start();
        t2.start();

        try {
            t1.join();
            t2.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        System.out.println("Balances: A=$" + accountA + " B=$" + accountB);
        System.out.println("[OK] No deadlock: circular wait prevented.\n");
    }

    private static final ReentrantLock REENTRANT_A = new ReentrantLock();
    private static final ReentrantLock REENTRANT_B = new ReentrantLock();

    private static void transferWithTryLock(
            String name, boolean aFirst, int amount) {

        boolean success = false;

        while (!success && !Thread.currentThread().isInterrupted()) {
            ReentrantLock first = aFirst ? REENTRANT_A : REENTRANT_B;
            ReentrantLock second = aFirst ? REENTRANT_B : REENTRANT_A;

            boolean firstLocked = false;

            try {
                firstLocked = first.tryLock(1, TimeUnit.SECONDS);

                if (!firstLocked) {
                    System.out.println("[" + name + "] First lock timed out; retrying");
                    continue;
                }

                System.out.println("[" + name + "] Locked first account");
                Thread.sleep(100);

                if (second.tryLock(1, TimeUnit.SECONDS)) {
                    try {
                        System.out.println("[" + name + "] Locked second account");

                        if (aFirst) {
                            accountA -= amount;
                            accountB += amount;
                            System.out.println("[" + name + "] Transfer A to B: $" + amount + " [OK]");
                        } else {
                            accountB -= amount;
                            accountA += amount;
                            System.out.println("[" + name + "] Transfer B to A: $" + amount + " [OK]");
                        }

                        success = true;
                    } finally {
                        second.unlock();
                    }
                } else {
                    System.out.println("[" + name + "] Second lock timed out; releasing and retrying");
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                return;
            } finally {
                if (firstLocked) {
                    first.unlock();
                }
            }

            if (!success) {
                try {
                    Thread.sleep(50);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    return;
                }
            }
        }
    }

    public static void fixedWithTryLock() {
        System.out.println("=== Fix 2: tryLock() with Timeout ===");
        System.out.println("If the second lock times out, release the first and retry.\n");

        accountA = 1000;
        accountB = 1000;

        Thread t1 = new Thread(
            () -> transferWithTryLock("T1", true, 100), "TryLock-T1");

        Thread t2 = new Thread(
            () -> transferWithTryLock("T2", false, 200), "TryLock-T2");

        t1.start();
        t2.start();

        try {
            t1.join();
            t2.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        System.out.println("Balances: A=$" + accountA + " B=$" + accountB);
        System.out.println("[OK] Both transfers completed without deadlock.\n");
    }

    public static void main(String[] args) {
        System.out.println("=== Deadlock Prevention Strategies ===");
        fixedWithOrdering();
        fixedWithTryLock();

        System.out.println("--- Summary ---");
        System.out.println("Fix 1: Consistent ordering prevents circular wait.");
        System.out.println("Fix 2: tryLock timeout lets threads release locks and retry.");
    }
}