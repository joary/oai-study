
The UE application starts from the same main-function as the eNodeB application,
but it runs different functions depending on the configuration.

# UE Main Thread:

Everything starts with the init_UE() function, which is actually a wrapper to start the thread UE_thread()

The main procedures executed at UE thread are:
 
UE_thread():
  - Create anothers threads by callling init_UE_threads()
    - The foollowing threads are created:
      - UE_thread_rxn_txnp4(): Process the received samples and generated the transmitted ones.
      - UE_thread_slot1_dl_processing(): 
      - UE_thread_synch(): performs band scanning and synchonization.
  - From here this thread will read samples from RF and send them to the respective thread depending on the processing state.
    - If ue is not synchronzed:
      - Get samples from RF
      - Unlocks the UE_thread_synch()
    - If ue is already synchronized:
      - Get samples from RF
      - Send samples to RF
      - Unlocks the UE_thread_rxn_txnp4() thread

# Frequency-Time Synchronization:

The initial cell-search through PSS and SSS are executed at UE_thread_synch() the main operations of this function are:

UE_thread_synch():
  - on syncmode: PSS
    - Call lte_sync_timefreq() -> Search for PSS
  - on syncmod: pbch
    - Call initial_sync() -> 
