
For the OAI eNodeB application, the file where main function is placed is {{lte-softmodem.c=/targets/RT/USER/lte-softmodem.c:1363}}.

The main operations executed at the lte-softmodem main function are:


1. Parse the command line options
2. Create the data-structures to hold configuration/operation
3. Initialize the logging system(s)
4. Fill the configurations
	1.  Configure the eNodeB parameters
	2.	Configure eNodeB interfaces with RF (or fronthaul) and MAC
		- This topic is discussed at section: **Interfaces (MAC and RF/Fronthaul)**
5. Start the thread(s)
	- This topic is discussed at section: **eNodeB Start**


## Interfaces (MAC and RF/Fronthaul)

The openair interface defines a set of functions and variables to interface with the lower (RF) and upper (MAC) laywers. 

These objects are initialized at two points in the code, the functions [init_eNB()](https://github.com/joary/openairinterface5g/tree/study/targets/RT/USER/lte-enb.c#L2054) and [l2_init()](https://github.com/joary/openairinterface5g/tree/study/openair2/LAYER2/MAC/main.c#L435).

1. [init_eNB()](https://github.com/joary/openairinterface5g/tree/study/targets/RT/USER/lte-enb.c#L2054): 
 - configres the interface between the eNodeB and RF (or Fronthaul) {{init_eNB=/targets/RT/USER/lte-enb.c:2010}}
2. [l2_init()](https://github.com/joary/openairinterface5g/tree/study/openair2/LAYER2/MAC/main.c#L435): 
 - configures the interface between eNodeB and MAC as shown {{l2_init=/openair2/LAYER2/MAC/main.c:435}}

Diving into the implementation of [init_eNB()](https://github.com/joary/openairinterface5g/tree/study/targets/RT/USER/lte-enb.c#L2054) function it can be seen as an initializer of some important
function and variables. Essentially these objects are chosed based on the node type.
Currently there are the following node types:

- eNodeB_3GPP:
	- The default LTE eNodeB application
- NGFI_RRU_IF5
	- Remote radio unit for a fronthaul transporting time-domain samples.
- eNodeB_3GPP_BBU
	- Base Band Unit (or Remote Cloud Center) for a fronthaul transporting time-domain samples.
- NGFI_RRU_IF4p5
	- Remote radio unit for a fronthaul transporting frequency-domain samples.
- NGFI_RCC_IF4p5
	- Base Band Unit (or Remote Cloud Center) for a fronthaul transporting frequency-domain samples.
- NGFI_RAU_IF4p5
	- Radio Agregation Unit (kind of a fronthaul router) for a fronthaul transporting frequency-domain samples.

#####BBU和RRU的区别
> **RRU是Remote Radio Unit 远端射频模块，BBU是Building Baseband Unit 室内基带处理单元。**
> 
> 基带BBU集中放置在机房，RRU可安装至楼层，BBU与RRU之间采用光纤传输，RRU再通过同轴电缆及功分器(耦合器)等连接至天线，即主干采用光纤，支路采用同轴电缆。
> 
> 对于下行方向：光纤从BBU直接连到RRU，BBU和RRU之间传输的是基带数字信号，这样基站可以控制某个用户的信号从指定的RRU通道发射出去，这样可以大大降低对本小区其他通道上用户的干扰。

>对于上行方向：用户手机信号被距离最近的通道收到，然后从这个通道经过光纤传到基站，这样也可以大大降低不同通道上用户之间的干扰。

For each of the nodes above the variables/functions composing the RF interface is configurated differently.
The following table hilight the configurations made.

| Function                 | Description                   | Who Calls  | Possible Val |
|--------------------------|-------------------------------|------------|--------------|
| eNB->do_prach            | execute the PRACH decoding procedures check at {{do_prach}} |  [rxtx()](https://github.com/joary/openairinterface5g/tree/study/targets/RT/USER/lte-enb.c#L652) | do_prach, NULL |
| eNB->start_rf            | initialize the Radio interface ex: (USRP,BLADERF,LMSSDR) | [eNB_thread_single()](https://github.com/joary/openairinterface5g/tree/study/targets/RT/USER/lte-enb.c#L1573) | start_rf, NULL |
| eNB->start_if            | initialize the Intermediate interface ex: (Fronthaul) | [eNB_thread_single()](https://github.com/joary/openairinterface5g/tree/study/targets/RT/USER/lte-enb.c#L1573) | start_if, NULL|
| eNB->proc_tx             | process the signal to be transmited on air | [rxtx()](https://github.com/joary/openairinterface5g/tree/study/targets/RT/USER/lte-enb.c#L652) | proc_tx_full, proc_tx_high, NULL |
| eNB->proc_uespec_rx      | eNB RX processin of UE-Specific signals | [rxtx()](https://github.com/joary/openairinterface5g/tree/study/targets/RT/USER/lte-enb.c#L652) | phy_procedures_eNB_uespec_RX, NULL |
| eNB->fep                 | eNB Uplink's DFT (initial SCFDM decode) | [phy_procedures_eNB_common_RX()](https://github.com/joary/openairinterface5g/tree/study/openair1/SCHED/phy_procedures_lte_eNb.c#L2859) | [eNB_fep_full()](https://github.com/joary/openairinterface5g/tree/study/openair1/SCHED/phy_procedures_lte_eNb.c#L2761), eNB_fep_rru_if5, NULL |
| eNB->td                  | Uplink decoding of ULSCH   | ulsch_decoding() | [ulsch_decoding_data()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/LTE_TRANSPORT/ulsch_decoding.c#L652), NULL |
| eNB->te                  | Downlink encoding of ULSCH | [pdsch_procedures()](https://github.com/joary/openairinterface5g/tree/study/openair1/SCHED/phy_procedures_lte_eNb.c#L938) | [dlsch_encoding()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/LTE_TRANSPORT/dlsch_coding.c#L560), NULL |
| eNB->tx_fh               | Send signal to fronthaul | [proc_tx_high()](https://github.com/joary/openairinterface5g/tree/study/targets/RT/USER/lte-enb.c#L478), [proc_tx_full()](https://github.com/joary/openairinterface5g/tree/study/targets/RT/USER/lte-enb.c#L492)  | [tx_fh_if5_mobipass()](https://github.com/joary/openairinterface5g/tree/study/targets/RT/USER/lte-enb.c#L428), [tx_fh_if5()](https://github.com/joary/openairinterface5g/tree/study/targets/RT/USER/lte-enb.c#L420), [tx_fh_if4p5()](https://github.com/joary/openairinterface5g/tree/study/targets/RT/USER/lte-enb.c#L444), NULL |
| eNB->rx_fh               | Receive signal from fronthaul | eNB_thread_fh(), [eNB_thread_single()](https://github.com/joary/openairinterface5g/tree/study/targets/RT/USER/lte-enb.c#L1573) | [rx_rf()](https://github.com/joary/openairinterface5g/tree/study/targets/RT/USER/lte-enb.c#L930), [rx_fh_slave()](https://github.com/joary/openairinterface5g/tree/study/targets/RT/USER/lte-enb.c#L1226), [rx_fh_if5()](https://github.com/joary/openairinterface5g/tree/study/targets/RT/USER/lte-enb.c#L1078), [rx_fh_if4p5()](https://github.com/joary/openairinterface5g/tree/study/targets/RT/USER/lte-enb.c#L1145), NULL |
| eNB->fh_asynch           | Get fronhtaul assynchronous messages | [eNB_thread_asynch_rxtx()](https://github.com/joary/openairinterface5g/tree/study/targets/RT/USER/lte-enb.c#L880) | [fh_if5_asynch_DL()](https://github.com/joary/openairinterface5g/tree/study/targets/RT/USER/lte-enb.c#L767), [fh_if4p5_asynch_DL()](https://github.com/joary/openairinterface5g/tree/study/targets/RT/USER/lte-enb.c#L805), [fh_if5_asynch_UL()](https://github.com/joary/openairinterface5g/tree/study/targets/RT/USER/lte-enb.c#L685), [fh_if4p5_asynch_UL()](https://github.com/joary/openairinterface5g/tree/study/targets/RT/USER/lte-enb.c#L724), NULL |
| eNB->rfdevice.host_type  | Configure the type of host this device is configured on | - | BBU_HOST, RRH_HOST |
| eNB->ifdevice.host_type  | Configure the type of host this device is configured on | - | BBU_HOST, RRH_HOST |

With these interface functions configured it is time to start the eNodeB application,
the next section will discuss the how this is made

# eNodeB Start 

The init_eNB calls an important functinon (**[init_eNB_proc()](https://github.com/wynter-wang/openairinterface5g/blob/affa19ce634218c361ad0cbd061e3775a335758d/targets/RT/USER/lte-enb.c#L1746)**), which will initialize 
eNB application.

There is two main operation modes: single and multi-thread.

- In the single thread mode a thread is created with the following function(**The default thread mode**):
  - eNB_thread_single
- In the multi-thread mode three main threads are created with the following functions:
  - **1 x** eNB_thread_FH
  - **2 x** eNB_thread_rxtx

Independent of the main operation mode there are some side threads that are created too:

* eNB_thread_prach
  * Decode the Physical Random Access Channel
    * prach_procedures:
* [eNB_thread_synch()](https://github.com/wynter-wang/openairinterface5g/blob/affa19ce634218c361ad0cbd061e3775a335758d/targets/RT/USER/lte-enb.c#L1826)
  * Runs initial synchronization like UE
		* [lte_sync_time_init()](https://github.com/wynter-wang/openairinterface5g/blob/affa19ce634218c361ad0cbd061e3775a335758d/targets/RT/USER/lte-enb.c#L1355)initialize variables for PSS detection
		* Run initial sync 
			* lte_sync_time_eNB()
			* The frame of PSS configure for FDD mode!
			* TDD mode is to be done.	(TDD模式的同步方式暂时没有，希望有人可以帮忙解答)

Also in the case where the node is a Remote Radio Unit the follwing thread is created: [eNB_thread_asynch_rxtx](https://github.com/wynter-wang/openairinterface5g/blob/c0a64ed506e5ae7d07a49b8c50ed80d4d711c7c2/targets/RT/USER/lte-enb.c#L1827)
``` 
if ((eNB->node_timing == synch_to_other) ||
	(eNB->node_function == NGFI_RRU_IF5) ||
	(eNB->node_function == NGFI_RRU_IF4p5))
      pthread_create( &proc->pthread_asynch_rxtx, attr_asynch, eNB_thread_asynch_rxtx, &eNB->proc ); /* 可以看到，只对RRU做了相应处理 */
```

###**_After these threads started the eNB application is pretty much ready to go._**

## eNodeB Single Thread Mode (*默认模式，重点关注*)

* eNB_thread_single  **单线程模式**
  * Called when the setup process uses single thread (**default**):
  * Functions called:
     * start_rf, start_if before the loop	// 加载硬件设备	
     * Check if the eNodeB is slave (???)(master/slave)   //主要是判断当前eNB是否为从设备，如果设从设备，要和其他设备进行同步(FDD无所谓，TDD有相应要求)
	     * If this is a slave eNodeB, try to synchronize on the DL frequency[hear](https://github.com/wynter-wang/openairinterface5g/blob/affa19ce634218c361ad0cbd061e3775a335758d/targets/RT/USER/lte-enb.c#L1630). But the conditions is just for **NGFI_RRU_IF5**
	     * if True: [wakeup_synch()](https://github.com/wynter-wang/openairinterface5g/blob/affa19ce634218c361ad0cbd061e3775a335758d/targets/RT/USER/lte-enb.c#L1654)	// 唤醒eNB进行与其他eNB或商用基站的同步   
    	
    * On the main loop:
     	* [rx_fh()](https://github.com/joary/openairinterface5g/tree/study/targets/RT/USER/lte-enb.c#L1512): if it exists
     	* [wakeup_slaves()](https://github.com/joary/openairinterface5g/tree/study/targets/RT/USER/lte-enb.c#L1292)
        * [rxtx()](https://github.com/joary/openairinterface5g/tree/study/targets/RT/USER/lte-enb.c#L652) lte-enb.c:574
          * [do_prach()](https://github.com/joary/openairinterface5g/tree/study/openair1/SCHED/phy_procedures_lte_eNb.c#L2817): if it exists and we are not RCC of IF4p5
          * [phy_procedures_eNB_common_RX()](https://github.com/joary/openairinterface5g/tree/study/openair1/SCHED/phy_procedures_lte_eNb.c#L2859) phy_procdures_eNB_common_RX:2835
            * [fep()](https://github.com/joary/openairinterface5g/tree/study/openair1/SCHED/phy_procedures_lte_eNb.c#L2886) if it exists
          * [proc_uespec_rx()](https://github.com/joary/openairinterface5g/tree/study/targets/RT/USER/lte-enb.c#L598): if it exists
            * UE-specific RX processing for subframe n
            * Pointer to: phy_procedures_eNB_uespec_RX
              * [compute_srs_pos()](https://github.com/joary/openairinterface5g/tree/study/openair1/SCHED/phy_procedures_lte_common.c#L1175)
              * [lte_srs_channel_estimation()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/LTE_ESTIMATION/lte_ul_channel_estimation.c#L672)
              * [pucch_procedures()](https://github.com/joary/openairinterface5g/tree/study/openair1/SCHED/phy_procedures_lte_eNb.c#L2113)
              * [process_Msg3()](https://github.com/joary/openairinterface5g/tree/study/openair1/SCHED/phy_procedures_lte_eNb.c#L1540) -> MAC connect
              * [rx_ulsch()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/LTE_TRANSPORT/ulsch_demodulation.c#L1573)
              * ulsch_decoding()
              * [extract_CQI()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/LTE_TRANSPORT/uci_tools.c#L165)
              * [lte_est_timing_advance_pusch()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/LTE_ESTIMATION/lte_adjust_sync.c#L232)
              * [process_HARQ_feedback()](https://github.com/joary/openairinterface5g/tree/study/openair1/SCHED/phy_procedures_lte_eNb.c#L1575)
          * [proc_tx()](https://github.com/joary/openairinterface5g/tree/study/targets/RT/USER/lte-enb.c#L609) if it exists (lte-enb:404)
            * [proc_tx_high0()](https://github.com/joary/openairinterface5g/tree/study/targets/RT/USER/lte-enb.c#L451)
              * [phy_procedures_eNB_TX()](https://github.com/joary/openairinterface5g/tree/study/openair1/SCHED/phy_procedures_lte_eNb.c#L1170) pry_procedures_lte_eNB.c:1146
                * UL_failure_indication - Emmit failure indication if exist
                * eNB_dlsch_ulsch_schedulre - Get scheduling information
                * [pmch_procedures()](https://github.com/joary/openairinterface5g/tree/study/openair1/SCHED/phy_procedures_lte_eNb.c#L431) - Procedures for the Phisical Multicast Channel
                * [common_signal_procedures()](https://github.com/joary/openairinterface5g/tree/study/openair1/SCHED/phy_procedures_lte_eNb.c#L513) - Generation of PSS/SSS/PBCH
                * max_xface->get_dci_sdu() - Get DCI information from MAC
                * For each connected UE existente on DCI
                  * [generate_eNB_dlsch_params()](https://github.com/joary/openairinterface5g/tree/study/openair1/SCHED/phy_procedures_lte_eNb.c#L699)
                * [phy_config_dedicated_eNB_step2()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/INIT/lte_init.c#L390) - 
                * For each connected UE existente on DCI
                  * [generate_eNB_ulsch_params()](https://github.com/joary/openairinterface5g/tree/study/openair1/SCHED/phy_procedures_lte_eNb.c#L843)
                * generate_dci_top() - Encode the DCI
                * [pdsch_procedures()](https://github.com/joary/openairinterface5g/tree/study/openair1/SCHED/phy_procedures_lte_eNb.c#L938) - Generate the shared channel with user data
                * generate_phich_top
            * [do_OFDM_mod_rt()](https://github.com/joary/openairinterface5g/tree/study/targets/RT/USER/lte-enb.c#L291)
              * [do_OFDM_mod_symbol()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/MODULATION/ofdm_mod.c#L286):
                * [beam_precoding()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/MODULATION/beamforming.c#L41)
                * [PHY_ofdm_mod()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/MODULATION/ofdm_mod.c#L79)
                  * [idft()](https://github.com/joary/openairinterface5g/tree/study/openair1/PHY/LTE_ESTIMATION/lte_dl_channel_estimation.c#L773)
            * [tx_fh()](https://github.com/joary/openairinterface5g/tree/study/targets/RT/USER/lte-enb.c#L488) if exists

## The eNodeB RF and IF interfaces:

## The slave eNodeB synchronization problem
> The problem is to be sloved! If someome have the solutions. Please do not hesitate to let me know.;)

## The main loop

# eNodeB Multi Thread Mode

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
