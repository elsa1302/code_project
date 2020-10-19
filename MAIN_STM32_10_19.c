/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * <h2><center>&copy; Copyright (c) 2020 STMicroelectronics.
  * All rights reserved.</center></h2>
  *
  * This software component is licensed by ST under BSD 3-Clause license,
  * the "License"; You may not use this file except in compliance with the
  * License. You may obtain a copy of the License at:
  *                        opensource.org/licenses/BSD-3-Clause
  *
  ******************************************************************************
  */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "tim.h"
#include "usart.h"
#include "gpio.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include <stdbool.h>
#include <string.h>
#include<stdio.h>
/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */
/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */
/*TRANSMITTING BOARD*/
#define tx
/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/

/* USER CODE BEGIN PV */
UART_HandleTypeDef huart2;

struct p1{
  	    int id;
  	    int length;
  		char msg[100];
  }tx1;
  struct p1* ptr;
  struct p1* rptr;
  struct p1* rxptr;

  /*buffer for transmission*/
  char buffer[sizeof(tx1)];
 /*buffer for reception*/
  char rx_buffer[sizeof(tx1)];
  uint16_t timerval;
  char uart_buf[50];
  int buflen;
/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
/* USER CODE BEGIN PFP */

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */
char cmp_[]="E\n";
uint8_t data_buffer[5];
char data_full[4];
uint8_t index_ = 0;
bool finished = 0;
/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

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
  MX_TIM16_Init();
  /* USER CODE BEGIN 2 */
  /* reception from GUI*/
  HAL_UART_Receive_IT(&huart2, data_buffer, sizeof(data_buffer));

  HAL_TIM_Base_Start(&htim16);
  /*get current time*/
  timerval=__HAL_TIM_GET_COUNTER(&htim16);
  //strcpy(( char*)tx1.msg,"sending and receiving\r\n");
   	 sprintf(tx1.msg,"data");
   	  	ptr = &tx1;
  /*transmission buffer*/
   	rptr=&buffer;
   	memcpy(rptr,ptr,sizeof(struct p1));
 /*reception buffer*/
    rxptr=&rx_buffer;
    memcpy(rxptr,ptr,sizeof(struct p1));

   #ifdef tx

 /* board 1 transmission and reception*/
    if(HAL_UART_Transmit_IT(&huart2,buffer,sizeof(buffer))==HAL_OK)
   {
 	   HAL_GPIO_TogglePin(GPIOB,GPIO_PIN_13);
   	   HAL_Delay(1000);
    }
  if(HAL_UART_Receive_IT(&huart2,rx_buffer,sizeof(rx_buffer))==HAL_OK)
    {
      HAL_GPIO_TogglePin(GPIOB,GPIO_PIN_13);
   	 HAL_Delay(500);
    }

   //show elapsed time

   	   timerval=__HAL_TIM_GET_COUNTER(&htim16)-timerval;
   	   buflen=sprintf(uart_buf,"\nExecution time taken is  %u us\r\n",timerval);
       HAL_UART_Transmit_IT(&huart2,(uint8_t*)uart_buf,buflen);


  #else
 /*board 2 reception and transmission*/
    if(HAL_UART_Receive_IT(&huart2,rx_buffer,sizeof(rx_buffer))==HAL_OK)
   	 {
   	    HAL_GPIO_TogglePin(GPIOB,GPIO_PIN_13);
   	    HAL_Delay(500);
   	  }
   	    if(HAL_UART_Transmit_IT(&huart2,buffer,sizeof(buffer))==HAL_OK)
   	   	    	  {
   	   	 	   HAL_GPIO_TogglePin(GPIOB,GPIO_PIN_13);
   	   	 	   HAL_Delay(1000);
   	   	    	  }

 		 //show elapsed time
 			 timerval=__HAL_TIM_GET_COUNTER(&htim16)-timerval;
 			 buflen=sprintf(uart_buf,"Execution time  is %u us\r\n",timerval);
 			HAL_UART_Transmit_IT(&huart2,(uint8_t*)uart_buf,buflen);

 #endif tx

  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
	  if(finished){
		  			if(strcmp(data_full, cmp_) == 0){
		  				HAL_UART_Transmit_IT(&huart2,(uint8_t*)uart_buf,buflen);
		  			}
		  			memset(data_full,'\0',strlen(data_full));
		  			finished = 0;
		  		}else{
		  			__NOP ();
		  		}

  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};
  RCC_PeriphCLKInitTypeDef PeriphClkInit = {0};

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_NONE;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }
  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_HSI;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV1;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_0) != HAL_OK)
  {
    Error_Handler();
  }
  PeriphClkInit.PeriphClockSelection = RCC_PERIPHCLK_TIM16;
  PeriphClkInit.Tim16ClockSelection = RCC_TIM16CLK_HCLK;
  if (HAL_RCCEx_PeriphCLKConfig(&PeriphClkInit) != HAL_OK)
  {
    Error_Handler();
  }
}

/* USER CODE BEGIN 4 */

void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
{
  /* Prevent unused argument(s) compilation warning */
  UNUSED(huart);

	if(data_buffer[0] != '\n'){
		data_full[index_] = data_buffer[0];
		index_++;
	}else{
		index_ = 0;
		finished = 1;
	}

}
/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */

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
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     tex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
