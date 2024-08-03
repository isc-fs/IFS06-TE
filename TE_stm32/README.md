
Sure, let's integrate the TX and RX functionality for the NRF24L01 into the given STM32 project structure. This involves creating two versions of `main.c`: one for the transmitter and one for the receiver. Below are the respective codes.

### Transmitter Code

#### main.c
```c
/* USER CODE BEGIN Header */
/**
 ******************************************************************************
 * @file           : main.c
 * @brief          : Main program body
 ******************************************************************************
 * @attention
 *
 * Copyright (c) 2022 STMicroelectronics.
 * All rights reserved.
 *
 * This software is licensed under terms that can be found in the LICENSE file
 * in the root directory of this software component.
 * If no LICENSE file comes with this software, it is provided AS-IS.
 *
 ******************************************************************************
 */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include "nrf24l01.h"
/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */
#define ID 0x300
/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
SPI_HandleTypeDef hspi1;

/* USER CODE BEGIN PV */
nrf24 nrfTx;

uint8_t txAddr[] = { 0xEA, 0xDD, 0xCC, 0xBB, 0xAA };
uint8_t txData[6];
/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_SPI1_Init(void);
/* USER CODE BEGIN PFP */

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */

/* USER CODE END 0 */

/**
 * @brief  The application entry point.
 * @retval int
 */
int main(void) {
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
    MX_SPI1_Init();
    /* USER CODE BEGIN 2 */
    // MODULE SETTINGS ----------------------------------------------
    nrfTx.CE_port = CE_GPIO_Port;
    nrfTx.CE_pin = CE_Pin;
    nrfTx.CSN_port = CSN_GPIO_Port;
    nrfTx.CSN_pin = CSN_Pin;
    nrfTx.IRQ_port = IRQ_GPIO_Port;
    nrfTx.IRQ_pin = IRQ_Pin;
    nrfTx.hSPIx = &hspi1;

    nrf24_init(&nrfTx);
    nrf24_setTxAddr(&nrfTx, txAddr);
    /* USER CODE END 2 */

    /* Infinite loop */
    /* USER CODE BEGIN WHILE */
    while (1) {
        uint16_t measurement1 = 1234;
        uint16_t measurement2 = 5678;

        txData[0] = (ID >> 8) & 0xFF;
        txData[1] = ID & 0xFF;
        txData[2] = (measurement1 >> 8) & 0xFF;
        txData[3] = measurement1 & 0xFF;
        txData[4] = (measurement2 >> 8) & 0xFF;
        txData[5] = measurement2 & 0xFF;

        nrf24_setMode(&nrfTx, txMode);
        if (nrf24_Transmit(&nrfTx, txData, sizeof(txData)) == 1) {
            nrf24_setMode(&nrfTx, standby);
            HAL_GPIO_TogglePin(LED_GPIO_Port, LED_Pin);
        }
        HAL_Delay(1000);
        /* USER CODE END WHILE */

        /* USER CODE BEGIN 3 */
    }
    /* USER CODE END 3 */
}

/**
 * @brief System Clock Configuration
 * @retval None
 */
void SystemClock_Config(void) {
    RCC_OscInitTypeDef RCC_OscInitStruct = { 0 };
    RCC_ClkInitTypeDef RCC_ClkInitStruct = { 0 };

    /** Initializes the RCC Oscillators according to the specified parameters
     * in the RCC_OscInitTypeDef structure.
     */
    RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
    RCC_OscInitStruct.HSIState = RCC_HSI_ON;
    RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
    RCC_OscInitStruct.PLL.PLLState = RCC_PLL_NONE;
    if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK) {
        Error_Handler();
    }

    /** Initializes the CPU, AHB and APB buses clocks
     */
    RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK | RCC_CLOCKTYPE_SYSCLK
            | RCC_CLOCKTYPE_PCLK1;
    RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_HSI;
    RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
    RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV1;

    if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_0) != HAL_OK) {
        Error_Handler();
    }
}

/**
 * @brief SPI1 Initialization Function
 * @param None
 * @retval None
 */
static void MX_SPI1_Init(void) {

    /* USER CODE BEGIN SPI1_Init 0 */

    /* USER CODE END SPI1_Init 0 */

    /* USER CODE BEGIN SPI1_Init 1 */

    /* USER CODE END SPI1_Init 1 */
    /* SPI1 parameter configuration*/
    hspi1.Instance = SPI1;
    hspi1.Init.Mode = SPI_MODE_MASTER;
    hspi1.Init.Direction = SPI_DIRECTION_2LINES;
    hspi1.Init.DataSize = SPI_DATASIZE_8BIT;
    hspi1.Init.CLKPolarity = SPI_POLARITY_LOW;
    hspi1.Init.CLKPhase = SPI_PHASE_1EDGE;
    hspi1.Init.NSS = SPI_NSS_SOFT;
    hspi1.Init.BaudRatePrescaler = SPI_BAUDRATEPRESCALER_2;
    hspi1.Init.FirstBit = SPI_FIRSTBIT_MSB;
    hspi1.Init.TIMode = SPI_TIMODE_DISABLE;
    hspi1.Init.CRCCalculation = SPI_CRCCALCULATION_DISABLE;
    hspi1.Init.CRCPolynomial = 7;
    hspi1.Init.CRCLength = SPI_CRC_LENGTH_DATASIZE;
    hspi1.Init.NSSPMode = SPI_NSS_PULSE_ENABLE;
    if (HAL_SPI_Init(&hspi1) != HAL_OK) {
        Error_Handler();
    }
    /* USER CODE BEGIN SPI1_Init 2 */

    /* USER CODE END SPI1_Init 2 */

}

/**
 * @brief GPIO Initialization Function
 * @param None
 * @retval None
 */
static void MX_GPIO_Init(void) {
    GPIO_InitTypeDef GPIO_InitStruct = { 0 };

    /* GPIO Ports Clock Enable */
    __HAL_RCC_GPIOB_CLK_ENABLE();
    __HAL_RCC_GPIOA_CLK_ENABLE();

    /*Configure GPIO pin Output Level */
    HAL_GPIO_WritePin(LED_GPIO_Port, LED_Pin, GPIO_PIN_RESET);

    /*Configure GPIO pin Output Level */
    HAL_GPIO_WritePin(CE_GPIO_Port, CE_Pin, GPIO_PIN_RESET);

    /*Configure GPIO pin Output Level */
    HAL_GPIO_WritePin(CSN_GPIO_Port, CSN_Pin, GPIO_PIN_SET);

    /*Configure GPIO pin : LED_Pin */
    GPIO_InitStruct.Pin = LED_Pin;
    GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
    HAL_GPIO_Init(LED_GPIO_Port, &GPIO_InitStruct);

    /*Configure GPIO pin : IRQ_Pin */
    GPIO_InitStruct.Pin = IRQ_Pin;
    GPIO_InitStruct.Mode = GPIO_MODE_IT_RISING;
    GPIO_InitStruct.Pull = GPIO_PULLUP;
    HAL_GPIO_Init(IRQ_GPIO_Port, &GPIO_InitStruct);

    /*Configure GPIO pin : CE_Pin */
    GPIO_InitStruct.Pin = CE_Pin;
    GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
    GPIO_InitStruct.Pull = GPIO_PULLDOWN;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
    HAL_GPIO_Init(CE_GPIO_Port, &GPIO_InitStruct);

    /*Configure GPIO pin : CSN_Pin */
    GPIO_InitStruct.Pin = CSN_Pin;
    GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
    GPIO_InitStruct.Pull = GPIO_PULLUP;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
    HAL_GPIO_Init(CSN_GPIO_Port, &GPIO_InitStruct);

}

/* USER CODE BEGIN 4 */

/* USER CODE END 4 */

/**
 * @brief  This function is executed in case of error occurrence.
 * @retval None
 */
void Error_Handler(void) {
    /* USER CODE BEGIN Error_Handler_Debug */
    /* User can add his own implementation to report the HAL error return state */
    __disable_irq();
    while (1) {
    }
    /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports

 the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */
```

### Receiver Code

#### main.c
```c
/* USER CODE BEGIN Header */
/**
 ******************************************************************************
 * @file           : main.c
 * @brief          : Main program body
 ******************************************************************************
 * @attention
 *
 * Copyright (c) 2022 STMicroelectronics.
 * All rights reserved.
 *
 * This software is licensed under terms that can be found in the LICENSE file
 * in the root directory of this software component.
 * If no LICENSE file comes with this software, it is provided AS-IS.
 *
 ******************************************************************************
 */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include "nrf24l01.h"
/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */
#define ID 0x300
/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
SPI_HandleTypeDef hspi1;

/* USER CODE BEGIN PV */
nrf24 nrfRx;

uint8_t rxAddr[] = { 0xEA, 0xDD, 0xCC, 0xBB, 0xAA };
uint8_t rxData[6];
/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_SPI1_Init(void);
/* USER CODE BEGIN PFP */

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */

/* USER CODE END 0 */

/**
 * @brief  The application entry point.
 * @retval int
 */
int main(void) {
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
    MX_SPI1_Init();
    /* USER CODE BEGIN 2 */
    // MODULE SETTINGS ----------------------------------------------
    nrfRx.CE_port = CE_GPIO_Port;
    nrfRx.CE_pin = CE_Pin;
    nrfRx.CSN_port = CSN_GPIO_Port;
    nrfRx.CSN_pin = CSN_Pin;
    nrfRx.IRQ_port = IRQ_GPIO_Port;
    nrfRx.IRQ_pin = IRQ_Pin;
    nrfRx.hSPIx = &hspi1;

    nrf24_init(&nrfRx);
    nrf24_setRxAddr(&nrfRx, rxAddr, 0);
    nrf24_setMode(&nrfRx, rxMode);
    /* USER CODE END 2 */

    /* Infinite loop */
    /* USER CODE BEGIN WHILE */
    while (1) {
        if (nrf24_DataReady(&nrfRx)) {
            nrf24_Receive(&nrfRx, rxData);
            uint16_t receivedID = (rxData[0] << 8) | rxData[1];
            uint16_t measurement1 = (rxData[2] << 8) | rxData[3];
            uint16_t measurement2 = (rxData[4] << 8) | rxData[5];

            if (receivedID == ID) {
                // Do something with measurement1 and measurement2
                HAL_GPIO_TogglePin(LED_GPIO_Port, LED_Pin);
            }
        }
        HAL_Delay(1000);
        /* USER CODE END WHILE */

        /* USER CODE BEGIN 3 */
    }
    /* USER CODE END 3 */
}

/**
 * @brief System Clock Configuration
 * @retval None
 */
void SystemClock_Config(void) {
    RCC_OscInitTypeDef RCC_OscInitStruct = { 0 };
    RCC_ClkInitTypeDef RCC_ClkInitStruct = { 0 };

    /** Initializes the RCC Oscillators according to the specified parameters
     * in the RCC_OscInitTypeDef structure.
     */
    RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
    RCC_OscInitStruct.HSIState = RCC_HSI_ON;
    RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
    RCC_OscInitStruct.PLL.PLLState = RCC_PLL_NONE;
    if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK) {
        Error_Handler();
    }

    /** Initializes the CPU, AHB and APB buses clocks
     */
    RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK | RCC_CLOCKTYPE_SYSCLK
            | RCC_CLOCKTYPE_PCLK1;
    RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_HSI;
    RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
    RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV1;

    if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_0) != HAL_OK) {
        Error_Handler();
    }
}

/**
 * @brief SPI1 Initialization Function
 * @param None
 * @retval None
 */
static void MX_SPI1_Init(void) {

    /* USER CODE BEGIN SPI1_Init 0 */

    /* USER CODE END SPI1_Init 0 */

    /* USER CODE BEGIN SPI1_Init 1 */

    /* USER CODE END SPI1_Init 1 */
    /* SPI1 parameter configuration*/
    hspi1.Instance = SPI1;
    hspi1.Init.Mode = SPI_MODE_MASTER;
    hspi1.Init.Direction = SPI_DIRECTION_2LINES;
    hspi1.Init.DataSize = SPI_DATASIZE_8BIT;
    hspi1.Init.CLKPolarity = SPI_POLARITY_LOW;
    hspi1.Init.CLKPhase = SPI_PHASE_1EDGE;
    hspi1.Init.NSS = SPI_NSS_SOFT;
    hspi1.Init.BaudRatePrescaler = SPI_BAUDRATEPRESCALER_2;
    hspi1.Init.FirstBit = SPI_FIRSTBIT_MSB;
    hspi1.Init.TIMode = SPI_TIMODE_DISABLE;
    hspi1.Init.CRCCalculation = SPI_CRCCALCULATION_DISABLE;
    hspi1.Init.CRCPolynomial = 7;
    hspi1.Init.CRCLength = SPI_CRC_LENGTH_DATASIZE;
    hspi1.Init.NSSPMode = SPI_NSS_PULSE_ENABLE;
    if (HAL_SPI_Init(&hspi1) != HAL_OK) {
        Error_Handler();
    }
    /* USER CODE BEGIN SPI1_Init 2 */

    /* USER CODE END SPI1_Init 2 */

}

/**
 * @brief GPIO Initialization Function
 * @param None
 * @retval None
 */
static void MX_GPIO_Init(void) {
    GPIO_InitTypeDef GPIO_InitStruct = { 0 };

    /* GPIO Ports Clock Enable */
    __HAL_RCC_GPIOB_CLK_ENABLE();
    __HAL_RCC_GPIOA_CLK_ENABLE();

    /*Configure GPIO pin Output Level */
    HAL_GPIO_WritePin(LED_GPIO_Port, LED_Pin, GPIO_PIN_RESET);

    /*Configure GPIO pin Output Level */
    HAL_GPIO_WritePin(CE_GPIO_Port, CE_Pin, GPIO_PIN_RESET);

    /*Configure GPIO pin Output Level */
    HAL_GPIO_WritePin(CSN_GPIO_Port, CSN_Pin, GPIO_PIN_SET);

    /*Configure GPIO pin : LED_Pin */
    GPIO_InitStruct.Pin = LED_Pin;
    GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
    HAL_GPIO_Init(LED_GPIO_Port, &GPIO_InitStruct);

    /*Configure GPIO pin : IRQ_Pin */
    GPIO_InitStruct.Pin = IRQ_Pin;
    GPIO_InitStruct.Mode = GPIO_MODE_IT_RISING;
    GPIO_InitStruct.Pull = GPIO_PULLUP;
    HAL_GPIO_Init(IRQ_GPIO_Port, &GPIO_InitStruct);

    /*Configure GPIO pin : CE_Pin */
    GPIO_InitStruct.Pin = CE_Pin;
    GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
    GPIO_InitStruct.Pull = GPIO_PULLDOWN;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
    HAL_GPIO_Init(CE_GPIO_Port, &GPIO_InitStruct);

    /*Configure GPIO pin : CSN_Pin */
    GPIO_InitStruct.Pin = CSN_Pin;
    GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
    GPIO_InitStruct.Pull = GPIO_PULLUP;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
    HAL_GPIO_Init(CSN_GPIO_Port, &GPIO_InitStruct);

}

/* USER CODE BEGIN 4 */

/* USER CODE END 4 */

/**
 * @brief  This function is executed in case of error occurrence.
 * @retval None
 */
void Error_Handler(void) {
    /* USER CODE BEGIN Error_Handler_Debug */
    /* User can

 add his own implementation to report the HAL error return state */
    __disable_irq();
    while (1) {
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
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */
```

#### nrf24l01.h
```c
#ifndef NRF24L01_H
#define NRF24L01_H

#include "main.h"
#include "stm32f1xx_hal.h"

typedef enum {
    txMode,
    rxMode,
    standby
} nrf24_mode;

typedef struct {
    SPI_HandleTypeDef *hSPIx;
    GPIO_TypeDef *CE_port;
    uint16_t CE_pin;
    GPIO_TypeDef *CSN_port;
    uint16_t CSN_pin;
    GPIO_TypeDef *IRQ_port;
    uint16_t IRQ_pin;
} nrf24;

void nrf24_init(nrf24 *dev);
void nrf24_setTxAddr(nrf24 *dev, uint8_t *addr);
void nrf24_setRxAddr(nrf24 *dev, uint8_t *addr, uint8_t pipe);
void nrf24_setMode(nrf24 *dev, nrf24_mode mode);
uint8_t nrf24_Transmit(nrf24 *dev, uint8_t *data, uint8_t length);
uint8_t nrf24_DataReady(nrf24 *dev);
void nrf24_Receive(nrf24 *dev, uint8_t *data);

#endif // NRF24L01_H
```

#### nrf24l01.c
```c
#include "nrf24l01.h"
#include "stm32f1xx_hal.h"

void nrf24_init(nrf24 *dev) {
    HAL_GPIO_WritePin(dev->CSN_port, dev->CSN_pin, GPIO_PIN_SET);
    HAL_GPIO_WritePin(dev->CE_port, dev->CE_pin, GPIO_PIN_RESET);
}

void nrf24_setTxAddr(nrf24 *dev, uint8_t *addr) {
    HAL_GPIO_WritePin(dev->CSN_port, dev->CSN_pin, GPIO_PIN_RESET);
    uint8_t command[] = {0x20 | 0x10, addr[0], addr[1], addr[2], addr[3], addr[4]};
    HAL_SPI_Transmit(dev->hSPIx, command, sizeof(command), HAL_MAX_DELAY);
    HAL_GPIO_WritePin(dev->CSN_port, dev->CSN_pin, GPIO_PIN_SET);
}

void nrf24_setRxAddr(nrf24 *dev, uint8_t *addr, uint8_t pipe) {
    HAL_GPIO_WritePin(dev->CSN_port, dev->CSN_pin, GPIO_PIN_RESET);
    uint8_t command[] = {0x20 | (0x0A + pipe), addr[0], addr[1], addr[2], addr[3], addr[4]};
    HAL_SPI_Transmit(dev->hSPIx, command, sizeof(command), HAL_MAX_DELAY);
    HAL_GPIO_WritePin(dev->CSN_port, dev->CSN_pin, GPIO_PIN_SET);
}

void nrf24_setMode(nrf24 *dev, nrf24_mode mode) {
    HAL_GPIO_WritePin(dev->CSN_port, dev->CSN_pin, GPIO_PIN_RESET);
    uint8_t command = 0x20 | 0x00;
    HAL_SPI_Transmit(dev->hSPIx, &command, 1, HAL_MAX_DELAY);

    uint8_t config;
    HAL_SPI_Receive(dev->hSPIx, &config, 1, HAL_MAX_DELAY);
    HAL_GPIO_WritePin(dev->CSN_port, dev->CSN_pin, GPIO_PIN_SET);

    if (mode == txMode) {
        config &= ~(1 << 0);
    } else if (mode == rxMode) {
        config |= (1 << 0);
    }

    HAL_GPIO_WritePin(dev->CSN_port, dev->CSN_pin, GPIO_PIN_RESET);
    uint8_t newConfig[] = {0x20 | 0x00, config};
    HAL_SPI_Transmit(dev->hSPIx, newConfig, sizeof(newConfig), HAL_MAX_DELAY);
    HAL_GPIO_WritePin(dev->CSN_port, dev->CSN_pin, GPIO_PIN_SET);

    if (mode == txMode || mode == rxMode) {
        HAL_GPIO_WritePin(dev->CE_port, dev->CE_pin, GPIO_PIN_SET);
    } else {
        HAL_GPIO_WritePin(dev->CE_port, dev->CE_pin, GPIO_PIN_RESET);
    }
}

uint8_t nrf24_Transmit(nrf24 *dev, uint8_t *data, uint8_t length) {
    HAL_GPIO_WritePin(dev->CSN_port, dev->CSN_pin, GPIO_PIN_RESET);
    uint8_t command = 0xA0;
    HAL_SPI_Transmit(dev->hSPIx, &command, 1, HAL_MAX_DELAY);
    HAL_SPI_Transmit(dev->hSPIx, data, length, HAL_MAX_DELAY);
    HAL_GPIO_WritePin(dev->CSN_port, dev->CSN_pin, GPIO_PIN_SET);

    HAL_GPIO_WritePin(dev->CE_port, dev->CE_pin, GPIO_PIN_SET);
    HAL_Delay(10);
    HAL_GPIO_WritePin(dev->CE_port, dev->CE_pin, GPIO_PIN_RESET);

    uint8_t status;
    HAL_GPIO_WritePin(dev->CSN_port, dev->CSN_pin, GPIO_PIN_RESET);
    command = 0x07;
    HAL_SPI_Transmit(dev->hSPIx, &command, 1, HAL_MAX_DELAY);
    HAL_SPI_Receive(dev->hSPIx, &status, 1, HAL_MAX_DELAY);
    HAL_GPIO_WritePin(dev->CSN_port, dev->CSN_pin, GPIO_PIN_SET);

    return (status & (1 << 5)) ? 1 : 0;
}

uint8_t nrf24_DataReady(nrf24 *dev) {
    uint8_t status;
    HAL_GPIO_WritePin(dev->CSN_port, dev->CSN_pin, GPIO_PIN_RESET);
    uint8_t command = 0x07;
    HAL_SPI_Transmit(dev->hSPIx, &command, 1, HAL_MAX_DELAY);
    HAL_SPI_Receive(dev->hSPIx, &status, 1, HAL_MAX_DELAY);
    HAL_GPIO_WritePin(dev->CSN_port, dev->CSN_pin, GPIO_PIN_SET);

    return status & (1 << 6);
}

void nrf24_Receive(nrf24 *dev, uint8_t *data) {
    HAL_GPIO_WritePin(dev->CSN_port, dev->CSN_pin, GPIO_PIN_RESET);
    uint8_t command = 0x61;
    HAL_SPI_Transmit(dev->hSPIx, &command, 1, HAL_MAX_DELAY);
    HAL_SPI_Receive(dev->hSPIx, data, 6, HAL_MAX_DELAY);
    HAL_GPIO_WritePin(dev->CSN_port, dev->CSN_pin, GPIO_PIN_SET);

    HAL_GPIO_WritePin(dev->CSN_port, dev->CSN_pin, GPIO_PIN_RESET);
    command = 0x27;
    uint8_t clear = 0x40;
    HAL_SPI_Transmit(dev->hSPIx, &command, 1, HAL_MAX_DELAY);
    HAL_SPI_Transmit(dev->hSPIx, &clear, 1, HAL_MAX_DELAY);
    HAL_GPIO_WritePin(dev->CSN_port, dev->CSN_pin, GPIO_PIN_SET);
}
```

### Code Explanation
1. **nrf24l01.h and nrf24l01.c**:
   - Defines the nrf24 structure and provides functions for initializing, setting addresses, setting modes, transmitting, checking for data readiness, and receiving data using the nRF24L01 module.
2. **Transmitter main.c**:
   - Sets up the nRF24L01 module in transmission mode.
   - Transmits data every second, and toggles an LED on successful transmission.
3. **Receiver main.c**:
   - Sets up the nRF24L01 module in receive mode.
   - Checks for data readiness and processes the received data, toggling an LED if the received ID matches the predefined ID.
