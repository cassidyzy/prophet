import re

from utils import crawler


class StockMoneyFlow:
    def __init__(self, symbol, name):
        self.symbol = symbol
        self.name = name
        self._crawl4Attrs(symbol)
    
    def _crawl4Attrs(self, symbol):
        url = "http://vip.stock.finance.sina.com.cn/quotes_service/api/jsonp.php/varmoneyFlowData=/MoneyFlow.ssi_ssfx_flzjtj?daima=%s&gettime=1" % symbol
        html = crawler.crawl(url)
        if html is None:
            self.state = 0
            return
        else:
            self.state = 1

        superbig_volume_in = self._reg4Value(html, "r0_in")
        if superbig_volume_in is not None:
            self.superbig_volume_in = float(superbig_volume_in)
        superbig_volume_out = self._reg4Value(html, "r0_in")
        if superbig_volume_out is not None:
            self.superbig_volume_out = float(superbig_volume_out)

        big_volume_in = self._reg4Value(html, "r1_in")
        if big_volume_in is not None:
            self.big_volume_in = float(big_volume_in)
        big_volume_out = self._reg4Value(html, "r1_out")
        if big_volume_out is not None:
            self.big_volume_out = float(big_volume_out)

        small_volume_in = self._reg4Value(html, "r2_in")
        if small_volume_in is not None:
            self.small_volume_in = float(small_volume_in)
        small_volume_out = self._reg4Value(html, "r2_out")
        if small_volume_out is not None:
            self.small_volume_out = float(small_volume_out)

        supersmall_volume_in = self._reg4Value(html, "r3_in")
        if supersmall_volume_in is not None:
            self.supersmall_volume_in = float(supersmall_volume_in)
        supersmall_volume_out = self._reg4Value(html, "r3_out")
        if supersmall_volume_out is not None:
            self.supersmall_volume_out = float(supersmall_volume_out)

        total_volume = self._reg4Value(html, "volume")
        if total_volume is not None:
            self.total_volume = float(total_volume)

        changeratio = self._reg4Value(html, "changeratio")
        if changeratio is not None:
            self.changeratio = float(changeratio)

        turnover = self._reg4Value(html, "turnover")
        if turnover is not None:
            self.turnover = float(turnover)

        superbig_angle = self._reg4Value(html, "r0x_ratio")
        if superbig_angle is not None:
            self.superbig_angle = float(superbig_angle)

        opendate = self._reg4Value(html, "opendate")
        if opendate is not None:
            self.opendate = opendate

    def _reg4Value(self, html, key):
        m = re.search(r'%s:"([^"]*)"' % key, html)
        if m:
            return m.group(1)
        else:
            return None

    def isValid(self):
        return self.state == 1

    def __str__(self):
        return "%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s" % (self.symbol, self.name, self.state, self.superbig_volume_in, self.superbig_volume_out, self.big_volume_in, self.big_volume_out, self.small_volume_in, self.small_volume_out, self.supersmall_volume_in, self.supersmall_volume_out, self.changeratio, self.total_volume, self.turnover, self.superbig_angle)

