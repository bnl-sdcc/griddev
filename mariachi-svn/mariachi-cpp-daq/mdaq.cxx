#include <iostream>
#include "./ftd2xx.h"
using namespace std;

FT_STATUS m_open_FPGA_device(FT_HANDLE*);
FT_STATUS m_send_FPGA_command(FT_HANDLE,unsigned char,int*,int**);
const unsigned char MDAQ_RESET_COUNTERS = 0xC0;
const unsigned char MDAQ_READ_CURRENT  = 0x80;
const unsigned char MDAQ_READ_PREVIOUS = 0x90; 
const unsigned char MDAQ_MAP           = 0x41;

char pFPGA_iface[] = "Morphic-IC B";

const int kMAX_CNTRS = 32; 

int main(int argc, char *argv[])
{
  FT_STATUS ftStatus;
  FT_HANDLE ftHandle;
  int i, n;
  int *counter;

  // Initialization

  ftStatus = m_open_FPGA_device(&ftHandle);
  ftStatus = m_send_FPGA_command(ftHandle,MDAQ_RESET_COUNTERS,&n,&counter);
  if (ftStatus != FT_OK) {
    FT_Close(ftHandle);
    return 1;
  }

  for (i = 0; i < n; i++) {
    printf("#%02d value %d\n",i+1,counter[i]);
  }
  
  // Main loop

  int sec = 0;
  for (i = 0; i < 60; i++) {
    //ftStatus = m_send_FPGA_command(ftHandle,MDAQ_READ_CURRENT,&n,&counter);
    ftStatus = m_send_FPGA_command(ftHandle,MDAQ_READ_PREVIOUS,&n,&counter);
    if (ftStatus == FT_OK) {
      if (counter[11] > sec) {
	sec = counter[11];
	printf("n=%d, sec=%d, counts=%d, rate=%4.1f\n",
	       n,counter[11],counter[0],counter[0]*10/float(sec));
	printf("-- sec=%d, counts=%d\n",counter[23],counter[12]);
      }
    }
    usleep(100000);
  }

  // finishing

  FT_Close(ftHandle);
  return 0;
}

FT_STATUS m_open_FPGA_device(FT_HANDLE *pftHandle) {
  FT_STATUS ftStatus;
  FT_HANDLE ftHandle;
  DWORD     iNumDev;
  int       i;

  ftStatus = FT_CreateDeviceInfoList(&iNumDev);
  if (ftStatus != FT_OK) return ftStatus;

  if (iNumDev <= 0) {
    printf("m_open_FPGA_device, Err: No FPGA devices found\n");
    return FT_OTHER_ERROR;
  }

  char      cBufLD[iNumDev][64];
  char    *pcBufLD[iNumDev+1];

  for(i = 0; i < iNumDev; i++) {
    pcBufLD[i] = cBufLD[i];
  }
  pcBufLD[iNumDev] = 0;

  bool match = false;
  ftStatus = FT_ListDevices(pcBufLD, &iNumDev, FT_LIST_ALL | FT_OPEN_BY_DESCRIPTION);
  if (ftStatus == FT_OK) {
    printf("Devices found: %d\n",iNumDev);
    for (i = 0; i< iNumDev; i++) {
      // printf("DV %d %s\n", i, pcBufLD[i]);
      if (strcmp(pcBufLD[i],pFPGA_iface)==0) {
	printf("Matching device found %s\n",pFPGA_iface);
	match = true;
	break;
      }
    }
  }

  if (!match) {
    printf("No matching device found %s\n",pFPGA_iface);
    return FT_OTHER_ERROR;
  }

  ftStatus = FT_OpenEx(pFPGA_iface,FT_OPEN_BY_DESCRIPTION,&ftHandle);
  if(ftStatus != FT_OK) return ftStatus;

  ftStatus = FT_ResetDevice(ftHandle); // Reset
  if(ftStatus != FT_OK) return ftStatus;

  ftStatus = FT_SetBaudRate(ftHandle,9600); // Baud rate 9600
  if(ftStatus != FT_OK) return ftStatus;

  ftStatus = FT_SetDataCharacteristics(ftHandle,FT_BITS_8,FT_STOP_BITS_1,FT_PARITY_NONE);
  if(ftStatus != FT_OK) return ftStatus;

  ftStatus = FT_SetFlowControl(ftHandle,FT_FLOW_NONE,0,0); // Set flow control
  if(ftStatus != FT_OK) return ftStatus;

  ftStatus = FT_Purge(ftHandle,FT_PURGE_RX|FT_PURGE_TX); // Purge Rx/Tx buffers
  if(ftStatus != FT_OK) return ftStatus;

  usleep(20000); // sleep for 20ms

  ftStatus = FT_SetDtr(ftHandle);
  if(ftStatus != FT_OK) return ftStatus;

  ftStatus = FT_SetRts(ftHandle);
  if(ftStatus != FT_OK) return ftStatus;

  *pftHandle = ftHandle;
  return FT_OK;
}

FT_STATUS m_send_FPGA_command(FT_HANDLE ftHandle,unsigned char cmd=0x0,int *pn=0,int **pcounter=0) {
  unsigned char cWBuf[16];
  unsigned char cRBuf[kMAX_CNTRS*2];
  
  FT_STATUS ftStatus;
  DWORD     dwNWrit, dwNRead;

  int         i, j, n;
  static int  counter[kMAX_CNTRS];

  cWBuf[0] = cmd;

  ftStatus = FT_Write(ftHandle,cWBuf,1,&dwNWrit);
  if (ftStatus != FT_OK) return ftStatus;

  if (cmd == MDAQ_RESET_COUNTERS) {
    sleep(1);       // 1 sec
  } else {
    usleep(100000); // 0.1 sec
  }

  ftStatus = FT_GetQueueStatus(ftHandle,&dwNRead);
  if(ftStatus != FT_OK) return ftStatus;

  if (dwNRead > 2*kMAX_CNTRS) {
    cout << "m_send_FPGA_command, Err1\n";
    return FT_OTHER_ERROR;
  }
  if (dwNRead !=0 && dwNRead % 2 == 0) {
    cout << "m_send_FPGA_command, Err2: NRead is even " << dwNRead << endl;
    return FT_OTHER_ERROR;
  }
  
  ftStatus = FT_Read(ftHandle,cRBuf,dwNRead,&dwNRead);
  if(ftStatus != FT_OK) return ftStatus;

  n = 0;
  for(i = 1; i < dwNRead; i+=2) {
    counter[n] = (cRBuf[i+1]<<8)+cRBuf[i];
    n++;
  }

  if (pn) {
    *pn = n;
    *pcounter = counter;
  }

  // printf("command %X, n=%d, echo %X\n",cWBuf[0],dwNRead,cRBuf[0]);

  return FT_OK;

}
