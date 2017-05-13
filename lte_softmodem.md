
# Functions of the lte_softmode:

* void signal_handler(int sig)
* void reset_stats(FL_OBJECT *button, long arg)
* static void *scope_thread(void *arg)
* void* gps_thread (void *arg)
* void *emos_thread (void *arg)
* static void wait_system_ready (char *message, volatile int *start_flag)
* void *l2l1_task(void *arg)
* void do_OFDM_mod_rt(int subframe,PHY_VARS_eNB *phy_vars_eNB)
* static void* eNB_thread_tx( void* param )
* static void* eNB_thread_rx( void* param )
* void init_eNB_proc(void)
* void kill_eNB_proc(void)
* static void* eNB_thread( void* arg )
* static void get_options (int argc, char **argv)
* int setup_eNB_buffers(PHY_VARS_eNB **phy_vars_eNB, openair0_config_t * *openair0_cfg, openair0_rf_map rf_map[MAX_NUM_CCs])
* void reset_opp_meas(void) {
* void print_opp_meas(void) {

# Where threads are created? and what they do?

* In init_eNB_proc:
	* eNB_thread_tx : created @ 1641, defined @ 1064 - 1064+295
		* Configure the thread affinity
		* Do mutex and condition stuff
		* phy_procedures_eNB_TX() @ 1255 => ???
		* do_OFDM_mod_rt() @ 1273 => ???
	* eNB_thread_rx : created @ 1642, defined @ 1367
		* Configure the thread affinity
		* Do mutex and condition stuff
		* when subframe == S_FS 
			* phy_procedures_eNB_S_RX
		* when subframe == S_UL 
			* phy_procedures_eNB_RX
* In main:
	* scope_thread : created @ 3666, defined @ 550
	* emos_thread  : created @ 3677, defined @ 719
	* gps_thread   : created @ 3679, defined @ 649
	* UE_thread    : created @ 3717, defined @ extern
	* eNB_thread   : created @ 3750, defined @ 1770 - 1770+542
		* Get/Send Samples to the RF frontend
		* process the mutex lock
		* Execute Debug and Log procedures

# Main function from 2863 - 3916 :

```
	Initial Setup of parameters:
	logInit() => ???
	Get Command Line Parametes
	T_init() => ???
	set_glog() => Initialize the logs, see log.h for details
	set_taus_seed() => 
	set_comp_log() => ??? 
		::: for HW, PHY, OPT ...
	vcd_signal_dumper() => ??? 
		::: /tmp/openair_dump_UE.vcd and /tmp/openair_dump_eNB.vcd
	reset_opp_meas() => ???

lte_softmodem.c:3004 TODO: continue
```
	
