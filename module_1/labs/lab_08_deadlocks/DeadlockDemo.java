public class DeadlockDemo {
    private static final Object LOCK_A = new Object();
    private static final Object LOCK_B = new Object();

    private static int accountA = 1000;
    private static int accountB = 1000;

    public static void main(String[] args) {
        System.out.println("=== Deadlock Demo ===");
        System.out.println("Account A: $" + accountA);
        System.out.println("Account B: $" + accountB);
        System.out.println("\nStarting two transfers simultaneously...\n");

        Thread transfer1 = new Thread(() -> {
            System.out.println("[T1] Trying to lock Account A...");
            synchronized (LOCK_A) {
                System.out.println("[T1] Locked Account A [OK]");
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    return;
                }

                System.out.println("[T1] Trying to lock Account B...");
                synchronized (LOCK_B) {
                    System.out.println("[T1] Locked Account B [OK]");
                    accountA -= 100;
                    accountB += 100;
                    System.out.println("[T1] Transfer complete: A->B $100");
                }
            }
        }, "Transfer-A-to-B");

        Thread transfer2 = new Thread(() -> {
            System.out.println("[T2] Trying to lock Account B...");
            synchronized (LOCK_B) {
                System.out.println("[T2] Locked Account B [OK]");
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    return;
                }

                System.out.println("[T2] Trying to lock Account A...");
                synchronized (LOCK_A) {
                    System.out.println("[T2] Locked Account A [OK]");
                    accountB -= 200;
                    accountA += 200;
                    System.out.println("[T2] Transfer complete: B->A $200");
                }
            }
        }, "Transfer-B-to-A");

        transfer1.start();
        transfer2.start();

        try {
            transfer1.join(120000);
            transfer2.join(120000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        if (transfer1.isAlive() || transfer2.isAlive()) {
            System.out.println("\n[FATAL] DEADLOCK DETECTED!");
            System.out.println("Both threads are stuck waiting for each other.");
            System.out.println("Run jstack from a second terminal to inspect the deadlock.");
            System.out.println("  " + transfer1.getName() + ": " + transfer1.getState());
            System.out.println("  " + transfer2.getName() + ": " + transfer2.getState());
            System.out.println("\nWait-For Graph:");
            System.out.println("  T1 (holds A) -> waits for B -> held by T2");
            System.out.println("  T2 (holds B) -> waits for A -> held by T1");
            System.out.println("  CYCLE DETECTED -> Deadlock!");
            System.exit(1);
        } else {
            System.out.println("\n[OK] Both transfers completed successfully.");
            System.out.println("Account A: $" + accountA);
            System.out.println("Account B: $" + accountB);
        }
    }
}
