import itertools
from enum import IntEnum, auto

# m, p, s, 東南西北白發中の順でソートされて渡される前提
test_tehai = ['1m', '2m', '3m', '1p', '2p', '3p', '1s', '2s', '3s', 'to', 'to', 'to', 'na']
test_tsumo = 'na'
test_huro = [['1p', '1p', '1p', '1p'], ['4s', '4s', '4s']]

# 定義
SUUHAI = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
MPS = ['m', 'p', 's']
# JIHAI = ['to', 'na', 'sy', 'pe', 'hk', 'ht', 'ch']
KAZEHAI = ['to', 'na', 'sy', 'pe']
SANGENHAI = ['hk', 'ht', 'ch']
KOKUSHI = ['1m', '9m', '1p', '9p', '1s', '9s', 'to', 'na', 'sy', 'pe', 'hk', 'ht', 'ch']
RYUISO = ['2s', '3s', '4s', '6s', '8s', 'ht']
CHINRO = ['1m', '9m', '1p', '9p', '1s', '9s']


class Yaku(IntEnum):
    # 一翻役
    MENZEN = auto()
    RICHI = auto()
    IPPATSU = auto()
    YAKU_HAKU = auto()
    YAKU_HATU = auto()
    YAKU_CHUN = auto()
    YAKU_BA = auto()
    YAKU_JI = auto()
    PINHU = auto()
    TANYAO = auto()
    IPEKO = auto()
    HAITEI = auto()
    HOUTEI = auto()
    CHANKAN = auto()
    RINSHAN = auto()
    # 二翻役
    DOUBLE = auto()
    TOITOI = auto()
    SANANKO = auto()
    SANKOKU = auto()
    SANKAN = auto()
    SHOSAN = auto()
    HONRO = auto()
    SANJYUN = auto()
    ITTSU = auto()
    CHANTA = auto()
    CHITOI = auto()
    # 三翻役
    RYANPE = auto()
    HONITSU = auto()
    JYUNCHAN = auto()
    # 六翻役
    CHINITSU = auto()
    # 役満
    TENHO = auto()
    CHIHO = auto()
    KOKUSHI = auto()
    SUANKO = auto()
    DAISAN = auto()
    RYUISO = auto()
    TSUISO = auto()
    SHOSUSHI = auto()
    DAISUSHI = auto()
    CHINRO = auto()
    SUKANTSU = auto()
    CHUREN = auto()


class Kaze(IntEnum):
    TON = auto()
    NAN = auto()
    SYA = auto()
    PE = auto()


def get_unique_list(seq):
    seen = []
    return [x for x in seq if x not in seen and not seen.append(x)]


# 1雀頭4面子の判定（副露も含む）
def chk_jyan1_mentsu4(tehai: list, huro: list, lh: str):
    mentsu_num = len(huro)
    all_tehai = tehai + list(lh)

    tmp_jtl = []
    for i in range(len(all_tehai) - 1):
        if all_tehai[i] == all_tehai[i + 1]:
            tmp_jtl.append((all_tehai[i], all_tehai[i + 1]))

    tmp_jtl = get_unique_list(tmp_jtl)
    is_agari = False
    for jt in tmp_jtl:
        is_agari = chk_n_mentsu([x for x in tehai if x not in list(jt)], 4 - mentsu_num)
        if is_agari:
            break

    return is_agari


def chk_chitoi(tehai: list, huro: list, lh: str):
    if len(huro) != 0:
        return False

    all_tehai = tehai + list(lh)
    tmp_jtl = []
    for i in range(len(all_tehai) - 1):
        if all_tehai[i] == all_tehai[i + 1]:
            tmp_jtl.append((all_tehai[i], all_tehai[i + 1]))
    tmp_jtl = get_unique_list(tmp_jtl)
    return len(tmp_jtl) == 7


# 指定された手配配列からn個の面子を作れるかどうか
def chk_n_mentsu(tehai: list, n):
    if n == 0:
        return True

    h = tehai[0]
    is_suhai = h[0].isdecimal()
    if not is_suhai:
        if tehai.count(h) == 3:
            return chk_n_mentsu([x for x in tehai if x != h], n - 1)
        else:
            return False
    else:
        if tehai.count(h) == 3:
            return chk_n_mentsu([x for x in tehai if x != h], n - 1)
        else:
            if int(h[0]) < 8:
                nhl = [h, f"{int(h[0] + 1)}{h[1]}", f"{int(h[0] + 2)}{h[1]}"]
                if (nhl[1] in tehai) and (nhl[2] in tehai):
                    return chk_n_mentsu([x for x in tehai if x not in nhl], n - 1)
                else:
                    return False
            else:
                return False


def chk_n_anko_tehai(tehai: list, n=0):
    if len(tehai) == 0:
        return n
    h = tehai[0]
    if tehai.count(h) == 3:
        return chk_n_anko_tehai([x for x in tehai if x != h], n + 1)
    else:
        return chk_n_anko_tehai([x for x in tehai if x != h], n)


def chk_n_anko_huro(huro: list, n=0):
    if len(huro) == 0:
        return n
    hr = huro[0]
    h = hr[0]
    if 3 <= hr.count(h) <= 4:
        return chk_n_anko_huro(huro[1:], n + 1)
    else:
        return chk_n_anko_huro(huro[1:], n)


def chk_kokushi(tehai: list, huro: list, lh: str):
    if len(huro) != 0:
        return False

    all_tehai = tehai + list(lh)
    for h in KOKUSHI:
        c = all_tehai.count(h)
        if 1 <= c <= 2:
            continue
        else:
            return False

    return True


def chk_daisan(tehai: list, huro: list, lh: str):
    all_tehai = tehai + list(itertools.chain.from_iterable(huro)) + list(lh)
    return 3 <= all_tehai.count('hk') <= 4 and 3 <= all_tehai.count('ht') <= 4 and 3 <= all_tehai.count('ch') <= 4


def chk_target_only(tehai: list, huro: list, lh: str, target: list):
    all_tehai = tehai + huro + list(lh)
    return len([x for x in all_tehai if x not in target]) == 0


def chk_sushi(tehai: list, huro: list, lh: str):
    n_men = 0
    n_jyan = 0
    all_tehai = tehai + list(itertools.chain.from_iterable(huro)) + list(lh)
    for h in KAZEHAI:
        if all_tehai.count(h) // 3 == 1:
            n_men += 1
        elif all_tehai.count(h) == 2:
            n_jyan += 1

    if n_men == 4:
        return Yaku.DAISUSHI
    elif n_men == 3 and n_jyan == 1:
        return Yaku.SHOSUSHI
    else:
        return None


def chk_churen(tehai: list, huro: list, lh: str):
    if len(huro) != 0:
        return False
    if not chk_chinitsu(tehai, huro, lh):
        return False

    sl = [x[0] for x in tehai + list(lh)]
    return sl.count(1) >= 3 and sl.count(9) >= 3 and sl.count(2) >= 1 and sl.count(3) >= 1 and sl.count(
        4) >= 1 and sl.count(5) >= 1 and sl.count(6) >= 1 and sl.count(7) >= 1 and sl.count(8) >= 1


def chk_chinitsu(tehai: list, huro: list, lh: str):
    all_tehai = tehai + list(itertools.chain.from_iterable(huro)) + list(lh)
    return len(set([x[1] for x in all_tehai])) == 1


def yaku(tehai: list, huro: list, lh: str, jyun, jikaze, bakaze, is_tsumo):
    is_huro = len(huro) != 0
    is_oya = jikaze == Kaze.TON
    is_jyan1_mentsu4 = chk_jyan1_mentsu4(tehai, huro, lh)
    is_chitoi = chk_chitoi(tehai, huro, lh)
    is_jyun_1 = jyun == 1
    anko_num = chk_n_anko_tehai(tehai + list(lh) if is_tsumo else tehai)
    yaku_l = []
    # 役満
    # 天和,地和
    if is_jyun_1 and (is_jyan1_mentsu4 or is_chitoi):
        if is_oya:
            yaku_l.append(Yaku.TENHO)
        else:
            yaku_l.append(Yaku.CHIHO)

    # 国士無双
    if chk_kokushi(tehai, huro, lh):
        yaku_l.append(Yaku.KOKUSHI)

    # 四暗刻
    if is_jyan1_mentsu4 and anko_num == 4 and not is_huro:
        yaku_l.append(Yaku.SUANKO)

    # 大三元
    if is_jyan1_mentsu4 and chk_daisan(tehai, huro, lh):
        yaku_l.append(Yaku.DAISAN)

    # 緑一色
    if is_jyan1_mentsu4 and chk_target_only(tehai, huro, lh, RYUISO):
        yaku_l.append(Yaku.RYUISO)

    # 字一色
    if is_jyan1_mentsu4 and chk_target_only(tehai, huro, lh, KAZEHAI + SANGENHAI):
        yaku_l.append(Yaku.TSUISO)

    # 小四喜
    sushi = chk_sushi(tehai, huro, lh)
    if is_jyan1_mentsu4 and sushi is not None:
        yaku_l.append(sushi)

    # 清老頭
    if is_jyan1_mentsu4 and chk_target_only(tehai, huro, lh, CHINRO):
        yaku_l.append(Yaku.CHINRO)

    # 四槓子
    if is_jyan1_mentsu4 and sum([len(x) for x in huro]) == 16:
        yaku_l.append(Yaku.SUKANTSU)

    # 九蓮宝燈
    if is_jyan1_mentsu4 and chk_churen(tehai, huro, lh) and not is_huro:
        yaku_l.append(Yaku.CHUREN)
