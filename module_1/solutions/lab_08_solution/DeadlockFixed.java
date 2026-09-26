/**
 * Lab 08 - Deadlock Fixed (SOLUTION)
 */
import java.util.concurrent.locks.ReentrantLock;
import java.util.concurrent.TimeUnit;

public class DeadlockFixed {

    private static int accountA = 1000;
    private static int accountB = 1000;
    private static final Object LOCK_A = new Object();
    private static final Object LOCK_B = new Object();

    public static void fixedWithOrdering() {
        System.out.println("\n=== Fix 1: Consistent Lock Ordering ===\n");

        Thread t1 = new Thread(() -> {
            synchronized (LOCK_A) {
                System.out.println("[T1] Locked A");
                try { Thread.sleep(100); } catch (InterruptedException e) {}
                synchronized (LOCK_B) {
                    System.out.println("[T1] Locked B");
                    accountA -= 100;
                    accountB += 100;
                    System.out.println("[T1] Transfer A→B $100 [OK]");
                }
            }
        });

        Thread t2 = new Thread(() -> {
            synchronized (LOCK_A) {  // Same order as T1!
                System.out.println("[T2] Locked A");
                try { Thread.sleep(100); } catch (InterruptedException e) {}
                synchronized (LOCK_B) {
                    System.out.println("[T2] Locked B");
                    accountB -= 200;
                    accountA += 200;
                    System.out.println("[T2] Transfer B→A $200 [OK]");
                }
            }
        });

        t1.start(); t2.start();
        try { t1.join(); t2.join(); } catch (InterruptedException e) {}
        System.out.println("Balances: A=$" + accountA + " B=$" + accountB);
        System.out.println("[OK] No deadlock!\n");
    }

    private static final ReentrantLock RL_A = new ReentrantLock();
    private static final ReentrantLock RL_B = new ReentrantLock();

    public static void fixedWithTryLock() {
        System.out.println("=== Fix 2: tryLock() with Timeout ===\n");
        accountA = 1000; accountB = 1000;

        Thread t1 = new Thread(() -> {
            boolean success = false;
            while (!success) {
                try {
                    if (RL_A.tryLock(1, TimeUnit.SECONDS)) {
                        try {
                            System.out.println("[T1] Locked A");
                            Thread.sleep(100);
                            if (RL_B.tryLock(1, TimeUnit.SECONDS)) {
                                try {
                                    accountA -= 100; accountB += 100;
                                    System.out.println("[T1] Transfer A→B $100 [OK]");
                                    success = true;
                                } finally { RL_B.unlock(); }
                            } else {
                                System.out.println("[T1] Couldn't get B, retrying...");
                            }
                        } finally { RL_A.unlock(); }
                    }
                } catch (InterruptedException e) {}
            }
        });

        Thread t2 = new Thread(() -> {
            boolean success = false;
            while (!success) {
                try {
                    if (RL_B.tryLock(1, TimeUnit.SECONDS)) {
                        try {
                            System.out.println("[T2] Locked B");
                            Thread.sleep(100);
                            if (RL_A.tryLock(1, TimeUnit.SECONDS)) {
                                try {
                                    accountB -= 200; accountA += 200;
                                    System.out.println("[T2] Transfer B→A $200 [OK]");
                                    success = true;
                                } finally { RL_A.unlock(); }
                            } else {
                                System.out.println("[T2] Couldn't get A, retrying...");
                            }
                        } finally { RL_B.unlock(); }
                    }
                } catch (InterruptedException e) {}
            }
        });

        t1.start(); t2.start();
        try { t1.join(); t2.join(); } catch (InterruptedException e) {}
        System.out.println("Balances: A=$" + accountA + " B=$" + accountB);
        System.out.println("[OK] No deadlock!\n");
    }

    public static void main(String[] args) {
        fixedWithOrdering();
        fixedWithTryLock();
        System.out.println("Fix 1 breaks Circular Wait | Fix 2 breaks No Preemption");
    }
}
