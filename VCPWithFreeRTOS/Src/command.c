#include <stdio.h>
#include <string.h> /* memset() */
#include <stdlib.h> /* strtol() */
#include <stdint.h>
#include "main.h"

/************************************************************
 *  define
 ************************************************************/
// 有効コマンド受信回数
static uint32_t g_CmdRxCount = 0;

/** コマンド処理関数 */
typedef void (*cmdFnuc)(const char *s);

typedef struct {
	char *name;		/**< コマンド名 */
	uint8_t	len;	/**< コマンド名の長さ(効率化のために使用) */
	cmdFnuc	fn;		/**< コマンド処理関数 */
	char *info;		/**< 情報(ヘルプコマンド時に表示) */
} Command;

static void cmdInstruct(const char *s);
static void cmdUpdate(const char *s);
static void cmdHelp(const char *s);
static void cmdVersion(const char *s);
static void cmdSwitch(const char *s);
static void cmdSet(const char *s);
static void cmdGet(const char *s);
static void cmdDebug(const char *s);
static void cmdReboot(const char *s);

static const Command g_CommandTable[] = {
	{ "#0",		2,	cmdInstruct,"Instruct",					},
	{ "#1",		2,	cmdUpdate,	"Update",					},
	{ "-h",		2,	cmdHelp,	"Help",						},
	{ "-v",		2,	cmdVersion,	"Version",					},
	{ "sw",		2,	cmdSwitch,	"Get DIP Switch",			},
	{ "s",		1,	cmdSet,		"Set Param : s <p1> <p2>",	},
	{ "g",		1,	cmdGet,		"Get Param : g <p1>",		},
	{ "dbg",	3,	cmdDebug,	"Debug : dbg <p1> <p2>",	},
	{ "reb",	3,	cmdReboot,	"Reboot"					},
};

/************************************************************
 *  prototype
 ************************************************************/
/**
 * 2文字を16進数1バイトに変換する。
 * エラー処理は行わない。
 */
static uint8_t atoh(uint8_t c_h, uint8_t c_l);

/**
 * 複数パラメータ解析
 * 
 * 文字列sからnum個のパラメータを解析してparams[]に格納する。
 * 格納出来た個数を戻り値として返す。
 * パラメータは空白文字(" ")で区切られているものとする。
 * num個分の解析が終了するか、もしくは'\0'が来たら終了する。
 *
 * @param s 入力文字列(NULLでないこと)
 * @param params 解析結果配列(NULLでないこと)
 * @param num 解析する個数(0より大)
 * @return 解析できた個数
 * @note 解析可能な値はstrtol()で基数0指定時のものに限る。
 * @note また、解析結果はint型に丸められることに注意。
 * @note 引数の前提に記載した項目はチェックしない。
 */
static int getParam(const char *s, int params[], int num);

/************************************************************
 *  public functions
 ************************************************************/
void Command_exec(const char *rxCmdBuff)
{
	int cmdIndex;
	for (cmdIndex = 0; cmdIndex < ARRAY_SIZE(g_CommandTable); cmdIndex++) {
		const Command *p = &g_CommandTable[cmdIndex];
		if (strncmp(p->name, rxCmdBuff, p->len) == 0) {
			p->fn(&rxCmdBuff[p->len]);
			break;
		}
	}

	// 一致しなかった場合
	if (cmdIndex == ARRAY_SIZE(g_CommandTable)) {
		// 空行ならプロンプト'>'を表示
		if (rxCmdBuff[0] == '\n') {
			PRINTF(">");
		// 空行でないなら誤ったコマンドという旨を表示
		} else {
			PRINTF("Bad Type.\n");
		}
	}
}

/************************************************************/

static void cmdInstruct(const char *s)
{
	static uint8_t data_all[36];	// ローカル変数にするとスタックオーバーフロー
	uint8_t i;
	
	// 例: #001FFFFFFFFFFFFFFFF01FFFFFFFFFFFFFFFF01FFFFFFFFFFFFFFFF01FFFFFFFFFFFFFFFF\n
	// ※"#0"を除いたものが引数sにセットされている
	for (i = 0; i < 36; i++) {
		data_all[i] = atoh(s[i*2], s[i*2 + 1]);
	}
	
	// TODO: data_allを使用すること
	data_all[0] = data_all[1];
	
	g_CmdRxCount++;
	PRINTF("%d\n", g_CmdRxCount);
}

static void cmdUpdate(const char *s)
{
	PRINTF("Not Implemented.\n");
}

static void cmdHelp(const char *s)
{
	int i;
	for (i = 0; i < ARRAY_SIZE(g_CommandTable); i++) {
		const Command *p = &g_CommandTable[i];
		PRINTF("%s : %s\n", p->name, p->info);
	}
}

static void cmdVersion(const char *s)
{
	PRINTF("Not Implemented.\n");
}

static void cmdSwitch(const char *s)
{
	PRINTF("Not Implemented.\n");
}

static void cmdSet(const char *s)
{
	int i;
	int pnum = 0;
	int params[2];
	
	pnum = getParam(s, params, 2);
	
	PRINTF("pnum = %d\n", pnum);
	for (i = 0; i < pnum; i++) {
		PRINTF("params[%d] = %d\n", i, params[i]);
	}
	
	if (pnum != 2) {
		return;
	}
}

static void cmdGet(const char *s)
{
	PRINTF("Not Implemented.\n");
}

static void cmdDebug(const char *s)
{
	int i;
	int pnum = 0;
	int params[2];
	
	pnum = getParam(s, params, 2);
	
	PRINTF("pnum = %d\n", pnum);
	for (i = 0; i < pnum; i++) {
		PRINTF("params[%d] = %d\n", i, params[i]);
	}
	
	if (pnum != 2) {
		return;
	}
}

static void cmdReboot(const char *s)
{
	PRINTF("Not Implemented.\n");
}

/************************************************************
 *  prvaite functions
 ************************************************************/
static uint8_t atoh(uint8_t c_h, uint8_t c_l)
{
	uint8_t h, l;
	uint8_t hex = 0;
	
	if (('a' <= c_h) && (c_h <= 'f')) {
		h = c_h - 'a' + 10;
	} else if (('A' <= c_h) && (c_h <= 'F')) {
		h = c_h - 'A' + 10;
	} else if (('0' <= c_h) && (c_h <= '9')) {
		h = c_h - '0';
	} else {
		/* error */
		h = 0x00;
	}
	
	if (('a' <= c_l) && (c_l <= 'f')) {
		l = c_l - 'a' + 10;
	} else if (('A' <= c_l) && (c_l <= 'F')) {
		l = c_l - 'A' + 10;
	} else if (('0' <= c_l) && (c_l <= '9')) {
		l = c_l - '0';
	} else {
		/* error */
		l = 0x00;
	}
	
	hex = (h << 4) | (l & 0x0F);
	return hex;
}

static int getParam(const char *s, int params[], int num)
{
	int ok_num = 0;
	char *startp = (char*)s;
	char *endp = NULL;
	long val = 0;
	
	do {
		val = strtol(startp, &endp, 0);
		// 1文字以上読めているなら何かしら解析できている。
		if (startp != endp) {
			params[ok_num] = (int)val;
			ok_num++;
		// 何も解析できなかったけど文字列最後でもない。
		} else if (val == 0) {
			break;
		}
		startp = endp;
	} while ((endp != NULL) && (ok_num < num));
	
	return ok_num;
}
