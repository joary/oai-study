# Functions:

* uint8_t is_SR_subframe(PHY_VARS_eNB *phy_vars_eNB,uint8_t UE_id,uint8_t sched_subframe)
* int32_t add_ue(int16_t rnti, PHY_VARS_eNB *phy_vars_eNB)
* int mac_phy_remove_ue(module_id_t Mod_idP,rnti_t rntiP)
* int8_t find_next_ue_index(PHY_VARS_eNB *phy_vars_eNB)
* int get_ue_active_harq_pid(const uint8_t Mod_id,const uint8_t CC_id,const uint16_t rnti, const int frame, const uint8_t subframe,uint8_t *harq_pid,uint8_t *round,const uint8_t ul_flag)
* int16_t get_target_pusch_rx_power(const module_id_t module_idP, const uint8_t CC_id)
* int16_t get_target_pucch_rx_power(const module_id_t module_idP, const uint8_t CC_id)
* void phy_procedures_emos_eNB_TX(unsigned char subframe, PHY_VARS_eNB *phy_vars_eNB)
* void phy_procedures_eNB_S_RX(unsigned char sched_subframe,PHY_VARS_eNB *phy_vars_eNB,uint8_t abstraction_flag,relaying_type_t r_type)
* void phy_procedures_emos_eNB_RX(unsigned char subframe,PHY_VARS_eNB *phy_vars_eNB)
* void phy_eNB_lte_measurement_thresholds_test_and_report(instance_t instanceP, ral_threshold_phy_t* threshold_phy_pP, uint16_t valP)
* void phy_eNB_lte_check_measurement_thresholds(instance_t instanceP, ral_threshold_phy_t* threshold_phy_pP)
* void phy_procedures_eNB_TX(unsigned char sched_subframe,PHY_VARS_eNB *phy_vars_eNB,uint8_t abstraction_flag,
relaying_type_t r_type,PHY_VARS_RN *phy_vars_rn)
* void process_Msg3(PHY_VARS_eNB *phy_vars_eNB,uint8_t sched_subframe,uint8_t UE_id, uint8_t harq_pid)
* void process_HARQ_feedback(uint8_t UE_id,
uint8_t sched_subframe,
PHY_VARS_eNB *phy_vars_eNB,
uint8_t pusch_flag,
uint8_t *pucch_payload,
uint8_t pucch_sel,
uint8_t SR_payload)
* void get_n1_pucch_eNB(PHY_VARS_eNB *phy_vars_eNB,
uint8_t UE_id,
uint8_t sched_subframe,
int16_t *n1_pucch0,
int16_t *n1_pucch1,
int16_t *n1_pucch2,
int16_t *n1_pucch3)
* void prach_procedures(PHY_VARS_eNB *phy_vars_eNB,uint8_t sched_subframe,uint8_t abstraction_flag)
* void ulsch_decoding_procedures(unsigned char subframe, unsigned int i, PHY_VARS_eNB *phy_vars_eNB, unsigned char abstraction_flag)
* void pucch_procedures(const unsigned char sched_subframe,PHY_VARS_eNB *phy_vars_eNB,int UE_id,int harq_pid,const uint8_t abstraction_flag)
* void cba_procedures(const unsigned char sched_subframe,PHY_VARS_eNB *phy_vars_eNB,int UE_id,int harq_pid,const uint8_t abstraction_flag)
* void phy_procedures_eNB_RX(const unsigned char sched_subframe,PHY_VARS_eNB *phy_vars_eNB,const uint8_t abstraction_flag,const relaying_type_t r_type)
* int phy_procedures_RN_eNB_TX(unsigned char last_slot, unsigned char next_slot, relaying_type_t r_type)
* void phy_procedures_eNB_lte(unsigned char subframe,PHY_VARS_eNB **phy_vars_eNB,uint8_t abstraction_flag,
relaying_type_t r_type, PHY_VARS_RN *phy_vars_rn)

# phy_procedures_eNB_TX 517 - 1605

# phy_procedures_eNB_RX 2671 - 3295
