
For the OAI eNodeB application, the file where main function is placed is {{lte-softmodem.c=/targets/RT/USER/lte-softmodem.c:1363}}.
It is possible to make a list of the things it does:

1. Parse the command line options
2. Create the data-structures
1. Initialize the logging system(s)
3. Fill the configurations
  1. Configure the eNodeB parameters
  2. Configure eNodeB interfaces with RF (or fronthaul) and MAC
4. Start the thread(s).

## Interfaces (MAC and RF/Fronthaul)

In the startup configuration it is possible to find two points where the interface
functions are configured:

- l2_init(): configures the interface between eNodeB and MAC as shown {{l2_init=/openair2/LAYER2/MAC/main.c:435}}
- init_eNB(): 


Two really important functions are init_eNB() and l2_init().

Functions configured on init_eNB()


| Function                 | Description                   | Who Calls   |
==========================================================================
| eNB->do_prach            | do_prach;                     |             |
| eNB->fep                 | eNB_fep_full;                 |             |
| eNB->td                  | ulsch_decoding_data;          |             |
| eNB->te                  | dlsch_encoding;               |             |
| eNB->proc_uespec_rx      | phy_procedures_eNB_uespec_RX; |             |
| eNB->proc_tx             | proc_tx_full;                 | rxtx (eNB_thread_rxtx, eNB_thread_single) |
| eNB->tx_fh               | NULL;                         | tx_proc_full, tx_proc_high |
| eNB->rx_fh               | rx_rf;                        | eNB_thread_fh, eNB_thread_single |
| eNB->start_rf            | start_rf;                     |             |
| eNB->start_if            | NULL;                         |             |
| eNB->fh_asynch           | NULL;                         | eNB_thread_asynch_rxtx |
| eNB->rfdevice.host_type  | BBU_HOST;                     |             |
| eNB->ifdevice.host_type  | BBU_HOST;                     |             |


# eNodeB Start 

The init_eNB_proc starts some threads, wich can be listed:

* eNB_thread_prach
  * Always created
  * Functions called:
    * prach_procedures:
* eNB_thread_synch
  * Always created
  * Functions called:
    * Runs initial synchronization like UE
* eNB_thread_single
  * Called when the setup process uses single thread (default):
  * Functions called:
     * start_rf, start_if at the before the loop
     * Check if the eNodeB is slave (???)
     * On the main loop:
        * rx_fh()
        * wakeup_slaves()
        * rxtx()
* eNB_thread_rxtx
  * There are two threads of this type per Component Carrier (CC), one process the even subframes the other process the odd.
  * This thread receives the subframe **N** and sends the subframe **N+4**
  * Internaly this thread calls:
    * eNB->do_prach
    * phy_procedures_eNB_common_RX
    * proc_uespec_rx
    * proc_tx
* eNB_thread_FH
  * Actually get the samples from fronthaul, it calls:
    - rx_fh
      - trx_write_func
      - trx_read_func
    - wakeup_slaves
    - wakeup_rxtx
* eNB_thread_asynch_rxtx
  * Started when the functino split is IF5 or IF4p5 and node timing is synch_to_other
