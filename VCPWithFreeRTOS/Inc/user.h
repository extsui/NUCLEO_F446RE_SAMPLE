#ifndef USER_H
#define USER_H

/************************************************************
 *  共通
 ************************************************************/
#include <stdio.h>
#include <stdint.h>

#define PRINTF(...)	printf(__VA_ARGS__)
#define ARRAY_SIZE(x)	(sizeof(x)/sizeof(x[0]))

typedef enum {
	FALSE = 0,
	TRUE  = 1,
} boolean_t;

// 参考: https://qiita.com/takoke/items/9e53fe12d48caa49cd40
static inline void delay_us(uint32_t usec)
{
    while(usec > 0) {
        // NOP168回@168MHz≒1us
		//実際はループ処理がある。実測でdelay_us(100)≒102us。
        __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP");
        __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP");
        __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP");
        __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP");
        __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP");
        __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP");
        __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP");
        __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP");
        __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP");
        __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP");
        
        __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP");
        __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP");
        __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP");
        __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP");
        __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP");
        __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP");
		__asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP"); __asm("NOP");
        usec--;
    }
}

/************************************************************
 *  システム特化
 ************************************************************/
#define ARMOR_UPDATE_INTERVAL_MS	(2)		// 最小値は2ms。Fingerの点灯周期が16msなのでそこに合わせるべき?

#define ARMOR_PANEL_FRAME_SIZE		(216)	// [[[Head(1)+Body(8)]*Fingers(4)]*Armors(6)]

typedef struct {
	uint8_t data[ARMOR_PANEL_FRAME_SIZE];
} ArmorPanelFrame;

extern osMessageQId queueLedTxHandle;

// 入力パネル
typedef struct {
	uint16_t brightness;
	uint16_t cycle;
	uint16_t gain;
} InputPanel;

// 入力パネル値取得
void getInputPanel(InputPanel *panel);

#endif /* USER_H */
