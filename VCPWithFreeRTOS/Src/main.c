
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * This notice applies to any and all portions of this file
  * that are not between comment pairs USER CODE BEGIN and
  * USER CODE END. Other portions of this file, whether 
  * inserted by the user or by software development tools
  * are owned by their respective copyright owners.
  *
  * Copyright (c) 2018 STMicroelectronics International N.V. 
  * All rights reserved.
  *
  * Redistribution and use in source and binary forms, with or without 
  * modification, are permitted, provided that the following conditions are met:
  *
  * 1. Redistribution of source code must retain the above copyright notice, 
  *    this list of conditions and the following disclaimer.
  * 2. Redistributions in binary form must reproduce the above copyright notice,
  *    this list of conditions and the following disclaimer in the documentation
  *    and/or other materials provided with the distribution.
  * 3. Neither the name of STMicroelectronics nor the names of other 
  *    contributors to this software may be used to endorse or promote products 
  *    derived from this software without specific written permission.
  * 4. This software, including modifications and/or derivative works of this 
  *    software, must execute solely and exclusively on microcontroller or
  *    microprocessor devices manufactured by or for STMicroelectronics.
  * 5. Redistribution and use of this software other than as permitted under 
  *    this license is void and will automatically terminate your rights under 
  *    this license. 
  *
  * THIS SOFTWARE IS PROVIDED BY STMICROELECTRONICS AND CONTRIBUTORS "AS IS" 
  * AND ANY EXPRESS, IMPLIED OR STATUTORY WARRANTIES, INCLUDING, BUT NOT 
  * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
  * PARTICULAR PURPOSE AND NON-INFRINGEMENT OF THIRD PARTY INTELLECTUAL PROPERTY
  * RIGHTS ARE DISCLAIMED TO THE FULLEST EXTENT PERMITTED BY LAW. IN NO EVENT 
  * SHALL STMICROELECTRONICS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
  * INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
  * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, 
  * OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF 
  * LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING 
  * NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
  * EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
  *
  ******************************************************************************
  */
/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "stm32f4xx_hal.h"
#include "cmsis_os.h"
#include "usb_device.h"

/* USER CODE BEGIN Includes */
#include "usbd_cdc_if.h"
#include "user.h"
/* USER CODE END Includes */

/* Private variables ---------------------------------------------------------*/
ADC_HandleTypeDef hadc1;

I2C_HandleTypeDef hi2c1;

SPI_HandleTypeDef hspi2;

UART_HandleTypeDef huart2;

osThreadId defaultTaskHandle;
osThreadId ledTaskHandle;
osThreadId vcpDriverTaskHandle;
osMessageQId queueVcpRxHandle;
osMessageQId queueLedTxHandle;
osTimerId switchPollTimerHandle;

/* USER CODE BEGIN PV */
/* Private variables ---------------------------------------------------------*/

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_USART2_UART_Init(void);
static void MX_SPI2_Init(void);
static void MX_ADC1_Init(void);
static void MX_I2C1_Init(void);
void StartDefaultTask(void const * argument);
void StartLedTask(void const * argument);
void StartVcpDriverTask(void const * argument);
void switchPollCallback(void const * argument);

/* USER CODE BEGIN PFP */
/* Private function prototypes -----------------------------------------------*/

/* USER CODE END PFP */

/* USER CODE BEGIN 0 */
#ifdef __GNUC__
#define PUTCHAR_PROTOTYPE int __io_putchar(int ch)
#else
#define PUTCHAR_PROTOTYPE int fputc(int ch, FILE *f)
#endif /* __GNUC__ */
PUTCHAR_PROTOTYPE
{
  /* Place your implementation of fputc here */
  /* e.g. write a character to the USART1 and Loop until the end of transmission */
  HAL_UART_Transmit(&huart2, (uint8_t *)&ch, 1, 0xFFFF);

  return ch;
}

void VCP_ReceivedCallback(uint8_t *buf, uint16_t len)
{
	int i;
	portBASE_TYPE xHigherPriorityTaskWoken = pdFALSE;
	for (i = 0; i < len; i++) {
		xQueueSendFromISR(queueVcpRxHandle, (uint8_t*)&buf[i], &xHigherPriorityTaskWoken);
	}
	portYIELD_FROM_ISR(xHigherPriorityTaskWoken);
}

void vApplicationIdleHook(void)
{
	// TODO:
}

void OLED_WriteCommand(uint8_t command)
{
	uint8_t txBuff[2];
	txBuff[0] = 0x00;
	txBuff[1] = command;
	HAL_I2C_Master_Transmit(&hi2c1, (uint16_t)0x3C<<1, txBuff, 2, 0xFFFF);
	HAL_Delay(10);
}

void OLED_Init(void)
{
	HAL_Delay(100);
	OLED_WriteCommand(0x01);	// Clear Display
	HAL_Delay(20);
	OLED_WriteCommand(0x02);	// Return Home
	HAL_Delay(2);
	//OLED_WriteCommand(0x0F);	// Send Display ON Command
	OLED_WriteCommand(0x0C);	// Send Display ON Command (Blink=0, Cursor=0)
	HAL_Delay(2);
	OLED_WriteCommand(0x01);	// Clear Display
	HAL_Delay(20);
}	

void OLED_SetContrast(uint8_t brightness)
{
	OLED_WriteCommand(0x2A);	// RE=1
	OLED_WriteCommand(0x79);	// SD=1
	OLED_WriteCommand(0x81);	// コントラストセット
	OLED_WriteCommand(brightness);
	OLED_WriteCommand(0x78);	// SDを0に戻す
	OLED_WriteCommand(0x28);	// 0x2C=高文字 / 0x28=ノーマル
	HAL_Delay(100);
}

void OLED_WriteData(uint8_t data)
{
	uint8_t txBuff[2];
	txBuff[0] = 0x40;
	txBuff[1] = data;
	HAL_I2C_Master_Transmit(&hi2c1, (uint16_t)0x3C<<1, txBuff, 2, 0xFFFF);
	HAL_Delay(1);
}

void OLED_HelloWorld(void)
{
	int i;
	int len;
	char str1[16] = "I2C OLED YELLOW";
	char str2[16];
	
	len = strlen(str1);
	for (i = 0; i < len; i++) {
		OLED_WriteData(str1[i]);
	}
	
	while (1) {
		// 2行目の先頭
		OLED_WriteCommand(0x20 + 0x80);
		
		sprintf(str2, "%10u", HAL_GetTick());
		len = strlen(str2);
		for (i = 0; i < len; i++) {
			OLED_WriteData(str2[i]);
		}
	}
}

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  *
  * @retval None
  */
int main(void)
{
  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration----------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_USART2_UART_Init();
  MX_SPI2_Init();
  MX_ADC1_Init();
  MX_I2C1_Init();
  /* USER CODE BEGIN 2 */
	OLED_Init();
	OLED_SetContrast(255);
	OLED_HelloWorld();

  /* USER CODE END 2 */

  /* USER CODE BEGIN RTOS_MUTEX */
  /* add mutexes, ... */
  /* USER CODE END RTOS_MUTEX */

  /* USER CODE BEGIN RTOS_SEMAPHORES */
  /* add semaphores, ... */
  /* USER CODE END RTOS_SEMAPHORES */

  /* Create the timer(s) */
  /* definition and creation of switchPollTimer */
  osTimerDef(switchPollTimer, switchPollCallback);
  switchPollTimerHandle = osTimerCreate(osTimer(switchPollTimer), osTimerPeriodic, NULL);

  /* USER CODE BEGIN RTOS_TIMERS */
  /* start timers, add new ones, ... */
  osTimerStart(switchPollTimerHandle, 10);
  /* USER CODE END RTOS_TIMERS */

  /* Create the thread(s) */
  /* definition and creation of defaultTask */
  osThreadDef(defaultTask, StartDefaultTask, osPriorityNormal, 0, 128);
  defaultTaskHandle = osThreadCreate(osThread(defaultTask), NULL);

  /* definition and creation of ledTask */
  osThreadDef(ledTask, StartLedTask, osPriorityAboveNormal, 0, 128);
  ledTaskHandle = osThreadCreate(osThread(ledTask), NULL);

  /* definition and creation of vcpDriverTask */
  osThreadDef(vcpDriverTask, StartVcpDriverTask, osPriorityHigh, 0, 128);
  vcpDriverTaskHandle = osThreadCreate(osThread(vcpDriverTask), NULL);

  /* USER CODE BEGIN RTOS_THREADS */
  /* add threads, ... */
  /* USER CODE END RTOS_THREADS */

  /* Create the queue(s) */
  /* definition and creation of queueVcpRx */
/* what about the sizeof here??? cd native code */
  osMessageQDef(queueVcpRx, 512, uint8_t);
  queueVcpRxHandle = osMessageCreate(osMessageQ(queueVcpRx), NULL);

  /* definition and creation of queueLedTx */
/* what about the sizeof here??? cd native code */
  osMessageQDef(queueLedTx, 8, ArmorPanelFrame);
  queueLedTxHandle = osMessageCreate(osMessageQ(queueLedTx), NULL);

  /* USER CODE BEGIN RTOS_QUEUES */
  /* add queues, ... */
  /* USER CODE END RTOS_QUEUES */
 

  /* Start scheduler */
  osKernelStart();
  
  /* We should never get here as control is now taken by the scheduler */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {

  /* USER CODE END WHILE */

  /* USER CODE BEGIN 3 */

  }
  /* USER CODE END 3 */

}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{

  RCC_OscInitTypeDef RCC_OscInitStruct;
  RCC_ClkInitTypeDef RCC_ClkInitStruct;
  RCC_PeriphCLKInitTypeDef PeriphClkInitStruct;

    /**Configure the main internal regulator output voltage 
    */
  __HAL_RCC_PWR_CLK_ENABLE();

  __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE1);

    /**Initializes the CPU, AHB and APB busses clocks 
    */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSE;
  RCC_OscInitStruct.HSEState = RCC_HSE_ON;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSE;
  RCC_OscInitStruct.PLL.PLLM = 4;
  RCC_OscInitStruct.PLL.PLLN = 168;
  RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV2;
  RCC_OscInitStruct.PLL.PLLQ = 7;
  RCC_OscInitStruct.PLL.PLLR = 2;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    _Error_Handler(__FILE__, __LINE__);
  }

    /**Initializes the CPU, AHB and APB busses clocks 
    */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV4;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV2;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_5) != HAL_OK)
  {
    _Error_Handler(__FILE__, __LINE__);
  }

  PeriphClkInitStruct.PeriphClockSelection = RCC_PERIPHCLK_CLK48;
  PeriphClkInitStruct.Clk48ClockSelection = RCC_CLK48CLKSOURCE_PLLQ;
  if (HAL_RCCEx_PeriphCLKConfig(&PeriphClkInitStruct) != HAL_OK)
  {
    _Error_Handler(__FILE__, __LINE__);
  }

    /**Configure the Systick interrupt time 
    */
  HAL_SYSTICK_Config(HAL_RCC_GetHCLKFreq()/1000);

    /**Configure the Systick 
    */
  HAL_SYSTICK_CLKSourceConfig(SYSTICK_CLKSOURCE_HCLK);

  /* SysTick_IRQn interrupt configuration */
  HAL_NVIC_SetPriority(SysTick_IRQn, 15, 0);
}

/* ADC1 init function */
static void MX_ADC1_Init(void)
{

  ADC_ChannelConfTypeDef sConfig;

    /**Configure the global features of the ADC (Clock, Resolution, Data Alignment and number of conversion) 
    */
  hadc1.Instance = ADC1;
  hadc1.Init.ClockPrescaler = ADC_CLOCK_SYNC_PCLK_DIV4;
  hadc1.Init.Resolution = ADC_RESOLUTION_12B;
  hadc1.Init.ScanConvMode = DISABLE;
  hadc1.Init.ContinuousConvMode = DISABLE;
  hadc1.Init.DiscontinuousConvMode = DISABLE;
  hadc1.Init.ExternalTrigConvEdge = ADC_EXTERNALTRIGCONVEDGE_NONE;
  hadc1.Init.ExternalTrigConv = ADC_SOFTWARE_START;
  hadc1.Init.DataAlign = ADC_DATAALIGN_RIGHT;
  hadc1.Init.NbrOfConversion = 1;
  hadc1.Init.DMAContinuousRequests = DISABLE;
  hadc1.Init.EOCSelection = ADC_EOC_SINGLE_CONV;
  if (HAL_ADC_Init(&hadc1) != HAL_OK)
  {
    _Error_Handler(__FILE__, __LINE__);
  }

    /**Configure for the selected ADC regular channel its corresponding rank in the sequencer and its sample time. 
    */
  sConfig.Channel = ADC_CHANNEL_0;
  sConfig.Rank = 1;
  sConfig.SamplingTime = ADC_SAMPLETIME_3CYCLES;
  if (HAL_ADC_ConfigChannel(&hadc1, &sConfig) != HAL_OK)
  {
    _Error_Handler(__FILE__, __LINE__);
  }

}

/* I2C1 init function */
static void MX_I2C1_Init(void)
{

  hi2c1.Instance = I2C1;
  hi2c1.Init.ClockSpeed = 100000;
  hi2c1.Init.DutyCycle = I2C_DUTYCYCLE_2;
  hi2c1.Init.OwnAddress1 = 0;
  hi2c1.Init.AddressingMode = I2C_ADDRESSINGMODE_7BIT;
  hi2c1.Init.DualAddressMode = I2C_DUALADDRESS_DISABLE;
  hi2c1.Init.OwnAddress2 = 0;
  hi2c1.Init.GeneralCallMode = I2C_GENERALCALL_DISABLE;
  hi2c1.Init.NoStretchMode = I2C_NOSTRETCH_DISABLE;
  if (HAL_I2C_Init(&hi2c1) != HAL_OK)
  {
    _Error_Handler(__FILE__, __LINE__);
  }

}

/* SPI2 init function */
static void MX_SPI2_Init(void)
{

  /* SPI2 parameter configuration*/
  hspi2.Instance = SPI2;
  hspi2.Init.Mode = SPI_MODE_MASTER;
  hspi2.Init.Direction = SPI_DIRECTION_2LINES;
  hspi2.Init.DataSize = SPI_DATASIZE_8BIT;
  hspi2.Init.CLKPolarity = SPI_POLARITY_LOW;
  hspi2.Init.CLKPhase = SPI_PHASE_1EDGE;
  hspi2.Init.NSS = SPI_NSS_SOFT;
  hspi2.Init.BaudRatePrescaler = SPI_BAUDRATEPRESCALER_32;
  hspi2.Init.FirstBit = SPI_FIRSTBIT_LSB;
  hspi2.Init.TIMode = SPI_TIMODE_DISABLE;
  hspi2.Init.CRCCalculation = SPI_CRCCALCULATION_DISABLE;
  hspi2.Init.CRCPolynomial = 10;
  if (HAL_SPI_Init(&hspi2) != HAL_OK)
  {
    _Error_Handler(__FILE__, __LINE__);
  }

}

/* USART2 init function */
static void MX_USART2_UART_Init(void)
{

  huart2.Instance = USART2;
  huart2.Init.BaudRate = 115200;
  huart2.Init.WordLength = UART_WORDLENGTH_8B;
  huart2.Init.StopBits = UART_STOPBITS_1;
  huart2.Init.Parity = UART_PARITY_NONE;
  huart2.Init.Mode = UART_MODE_TX_RX;
  huart2.Init.HwFlowCtl = UART_HWCONTROL_NONE;
  huart2.Init.OverSampling = UART_OVERSAMPLING_16;
  if (HAL_UART_Init(&huart2) != HAL_OK)
  {
    _Error_Handler(__FILE__, __LINE__);
  }

}

/** Configure pins as 
        * Analog 
        * Input 
        * Output
        * EVENT_OUT
        * EXTI
*/
static void MX_GPIO_Init(void)
{

  GPIO_InitTypeDef GPIO_InitStruct;

  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOC_CLK_ENABLE();
  __HAL_RCC_GPIOH_CLK_ENABLE();
  __HAL_RCC_GPIOA_CLK_ENABLE();
  __HAL_RCC_GPIOB_CLK_ENABLE();

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(LATCH_GPIO_Port, LATCH_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(LD2_GPIO_Port, LD2_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pin : B1_Pin */
  GPIO_InitStruct.Pin = B1_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_IT_FALLING;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  HAL_GPIO_Init(B1_GPIO_Port, &GPIO_InitStruct);

  /*Configure GPIO pin : LATCH_Pin */
  GPIO_InitStruct.Pin = LATCH_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(LATCH_GPIO_Port, &GPIO_InitStruct);

  /*Configure GPIO pin : LD2_Pin */
  GPIO_InitStruct.Pin = LD2_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(LD2_GPIO_Port, &GPIO_InitStruct);

  /*Configure GPIO pins : AUTO_ADJ_Pin MODE_Pin */
  GPIO_InitStruct.Pin = AUTO_ADJ_Pin|MODE_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
  GPIO_InitStruct.Pull = GPIO_PULLUP;
  HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

}

/* USER CODE BEGIN 4 */

static uint16_t getAnalogValue(uint8_t ch)
{
	ADC_ChannelConfTypeDef sConfig;
	uint32_t analogCh0, analogCh1, analogCh4;
	
	sConfig.Rank = 1;
	sConfig.SamplingTime = ADC_SAMPLETIME_56CYCLES;
	
	if (ch == 0) {
		sConfig.Channel = ADC_CHANNEL_0;
		HAL_ADC_ConfigChannel(&hadc1, &sConfig);
		HAL_ADC_Start(&hadc1);
		HAL_ADC_PollForConversion(&hadc1, 10);
		analogCh0 = HAL_ADC_GetValue(&hadc1);
		return analogCh0;
		
	} else if (ch == 1) {
		sConfig.Channel = ADC_CHANNEL_1;
		HAL_ADC_ConfigChannel(&hadc1, &sConfig);
		HAL_ADC_Start(&hadc1);
		HAL_ADC_PollForConversion(&hadc1, 10);
		analogCh1 = HAL_ADC_GetValue(&hadc1);
		return analogCh1;
		
	} else if (ch == 4) {
		sConfig.Channel = ADC_CHANNEL_4;
		HAL_ADC_ConfigChannel(&hadc1, &sConfig);
		HAL_ADC_Start(&hadc1);
		HAL_ADC_PollForConversion(&hadc1, 10);
		analogCh4 = HAL_ADC_GetValue(&hadc1);
		return analogCh4;
		
	} else {
		return 0xFFFF;
	}
}

void getInputPanel(InputPanel *panel)
{
	// TODO: 同期なので時間がかかることに注意。
	// 最終的にはDMA転送にしてフィルタ付きにするべき。
	panel->brightness = getAnalogValue(1);
	panel->cycle = getAnalogValue(4);
	panel->gain = getAnalogValue(0);
}

/* USER CODE END 4 */

/* StartDefaultTask function */
void StartDefaultTask(void const * argument)
{
  /* init code for USB_DEVICE */
  MX_USB_DEVICE_Init();

  /* USER CODE BEGIN 5 */
  /* Infinite loop */
  for (;;)
  {
	uint32_t analogCh0, analogCh1, analogCh4;
	analogCh0 = getAnalogValue(0);
	analogCh1 = getAnalogValue(1);
	analogCh4 = getAnalogValue(4);
  
	PRINTF("%d %d %d\n", analogCh0, analogCh1, analogCh4);
	
	static ArmorPanelFrame frame;
	portBASE_TYPE xStatus;
	
	// 自動調整モードONの場合のみ輝度/周期コマンドを送信する
	if (HAL_GPIO_ReadPin(AUTO_ADJ_GPIO_Port, AUTO_ADJ_Pin) == GPIO_PIN_RESET) {
		osDelay(100);
		continue;
	}
	
	//////////////////////////////////////////////////
	//  輝度
	//////////////////////////////////////////////////
	// 12bitADC(0-4095) --> 8bit
	uint8_t brightness = (uint8_t)(analogCh1 >> 4);
	
	// 1Finger
	frame.data[0] = 0x02;
	memset(&frame.data[1], brightness, 8);
	// 1Armor(Finger*4)
	memcpy(&frame.data[9*1], &frame.data[0], 9);
	memcpy(&frame.data[9*2], &frame.data[0], 9);
	memcpy(&frame.data[9*3], &frame.data[0], 9);
	// 1ArmorPanel(Armor*6)
	memcpy(&frame.data[36*1], &frame.data[0], 36);
	memcpy(&frame.data[36*2], &frame.data[0], 36);
	memcpy(&frame.data[36*3], &frame.data[0], 36);
	memcpy(&frame.data[36*4], &frame.data[0], 36);
	memcpy(&frame.data[36*5], &frame.data[0], 36);
	
	// MEMO:
	// 当初はArmor1コマンド分36バイトを1要素としたキューを考えていたが、
	// 6要素でArmorPanel1コマンドになるので、間にVCPからのコマンドが
	// 割り込んでくる場合が普通に有りうる。
	// つまり、6要素は不可分なので、Armorコマンド6個分の計216バイトを
	// 1要素とする必要がある。
	xStatus = xQueueSend(queueLedTxHandle, (ArmorPanelFrame*)&frame, portMAX_DELAY);
	if (xStatus != pdPASS) {
		PRINTF("ERR: queueLedTxHandle is Full!\n");
	}
	
	//////////////////////////////////////////////////
	//  周期
	//////////////////////////////////////////////////
	// 12bitADC(0-4095) --> 500-5000
	//   base=500, range=4500
	uint16_t light_cycle = (uint16_t)((((analogCh4 * 1.0) / 4096) * 4500) + 500);
	
	// 1Finger
	frame.data[0] = 0x04;
	frame.data[1] = (uint8_t)((light_cycle & 0xFF00) >> 8);
	frame.data[2] = (uint8_t)((light_cycle & 0x00FF));
	memset(&frame.data[3], 0xFF, 5);
	// 1Armor(Finger*4)
	memcpy(&frame.data[9*1], &frame.data[0], 9);
	memcpy(&frame.data[9*2], &frame.data[0], 9);
	memcpy(&frame.data[9*3], &frame.data[0], 9);
	// 1ArmorPanel(Armor*6)
	memcpy(&frame.data[36*1], &frame.data[0], 36);
	memcpy(&frame.data[36*2], &frame.data[0], 36);
	memcpy(&frame.data[36*3], &frame.data[0], 36);
	memcpy(&frame.data[36*4], &frame.data[0], 36);
	memcpy(&frame.data[36*5], &frame.data[0], 36);
	
	xStatus = xQueueSend(queueLedTxHandle, (ArmorPanelFrame*)&frame, portMAX_DELAY);
	if (xStatus != pdPASS) {
		PRINTF("ERR: queueLedTxHandle is Full!\n");
	}
	
	osDelay(100);
  }
  /* USER CODE END 5 */ 
}

/* StartLedTask function */
void StartLedTask(void const * argument)
{
  /* USER CODE BEGIN StartLedTask */
	// 有効コマンド受信回数
	static uint32_t cmdRxCount = 0;
	
  /* Infinite loop */
  for(;;)
  {
	static ArmorPanelFrame frame;
	xQueueReceive(queueLedTxHandle, &frame, portMAX_DELAY);
	cmdRxCount++;
	
	// コマンド送信中のみLEDを点灯させる
	HAL_GPIO_WritePin(LD2_GPIO_Port, LD2_Pin, GPIO_PIN_SET);
	
	int i;
	for (i = 0; i < 6; i++) {
		HAL_SPI_Transmit(&hspi2, &frame.data[i*(sizeof(frame.data)/6)], sizeof(frame.data)/6, 0xFFFF);
		delay_us(150 * 2);
	}
	
	// データ送信から更新までは一定時間空ける必要がある
	osDelay(ARMOR_UPDATE_INTERVAL_MS);
	
	HAL_GPIO_WritePin(LATCH_GPIO_Port, LATCH_Pin, GPIO_PIN_SET);
	delay_us(10);
	HAL_GPIO_WritePin(LATCH_GPIO_Port, LATCH_Pin, GPIO_PIN_RESET);
	
	// LATCH後の遅延は絶対必要。ただし、最適な時間は要検討。
	// これがない場合は表示破壊等が多発する。
	osDelay(2);
	
	// デバッグ用。これを入れると通信速度がかなり下がることに注意。
	// 参考: 20KB/s->10KB/s
	//PRINTF("%d\n", cmdRxCount);
	
	HAL_GPIO_WritePin(LD2_GPIO_Port, LD2_Pin, GPIO_PIN_RESET);
  }
  /* USER CODE END StartLedTask */
}

/* StartVcpDriverTask function */
void StartVcpDriverTask(void const * argument)
{
  /* USER CODE BEGIN StartVcpDriverTask */
  /* Infinite loop */
  for(;;)
  {
	int i;
	int len = 0;
	static int rxCmdBuffIndex = 0;
	static uint8_t rxCmdBuff[512];
	
	len = uxQueueMessagesWaiting(queueVcpRxHandle);
	
	if (len >= 1) {
		for (i = 0; i < len; i++) {
			xQueueReceive(queueVcpRxHandle, &rxCmdBuff[rxCmdBuffIndex], 0);
			rxCmdBuffIndex++;
			
			// コマンド受信完了
			if (rxCmdBuff[rxCmdBuffIndex-1] == '\n') {
				extern void Command_exec(const char *rxCmdBuff);
				Command_exec((const char*)rxCmdBuff);
				
				// 次のコマンド受信待機
				memset(rxCmdBuff, 0, sizeof(rxCmdBuff));
				rxCmdBuffIndex = 0;
				break;
			}
		}
	}
	
    osDelay(1);
  }
  /* USER CODE END StartVcpDriverTask */
}

/* switchPollCallback function */
void switchPollCallback(void const * argument)
{
  /* USER CODE BEGIN switchPollCallback */
 	static GPIO_PinState pinPrevState = GPIO_PIN_SET;
	GPIO_PinState pin;
	
	pin = HAL_GPIO_ReadPin(MODE_GPIO_Port, MODE_Pin);
	
	// 押下(RESET)->リリース(SET)で確定
	if ((pinPrevState == GPIO_PIN_RESET) && (pin == GPIO_PIN_SET)) {
		g_ModeEvent = TRUE;
	}
	pinPrevState = pin;
	
  /* USER CODE END switchPollCallback */
}

/**
  * @brief  Period elapsed callback in non blocking mode
  * @note   This function is called  when TIM14 interrupt took place, inside
  * HAL_TIM_IRQHandler(). It makes a direct call to HAL_IncTick() to increment
  * a global variable "uwTick" used as application time base.
  * @param  htim : TIM handle
  * @retval None
  */
void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim)
{
  /* USER CODE BEGIN Callback 0 */

  /* USER CODE END Callback 0 */
  if (htim->Instance == TIM14) {
    HAL_IncTick();
  }
  /* USER CODE BEGIN Callback 1 */

  /* USER CODE END Callback 1 */
}

/**
  * @brief  This function is executed in case of error occurrence.
  * @param  file: The file name as string.
  * @param  line: The line in file as a number.
  * @retval None
  */
void _Error_Handler(char *file, int line)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  while(1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t* file, uint32_t line)
{ 
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     tex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */

/**
  * @}
  */

/**
  * @}
  */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
