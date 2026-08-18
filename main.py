import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.clock import Clock

class SMCTradingApp(App):
    def build(self):
        # मुख्य लेआउट (पूरे स्क्रीन का)
        self.main_layout = BoxLayout(
            orientation='vertical', 
            padding=[15, 20, 15, 20], 
            spacing=15
        )

        # 1. हेडर (ऐप टाइटल)
        self.title_label = Label(
            text="SMC AI TRADING SYSTEM\n[ BY VEER ]", 
            font_size='18sp', 
            bold=True, 
            size_hint_y=0.15,
            halign='center',
            valign='center'
        )
        self.title_label.bind(size=self.title_label.setter('text_size'))
        self.main_layout.add_widget(self.title_label)

        # 2. ग्रिड लेआउट - 5 कार्ड्स के लिए (समान दूरी के साथ)
        self.grid = GridLayout(
            cols=1, 
            spacing=12, 
            size_hint_y=0.85
        )
        self.main_layout.add_widget(self.grid)

        # 5 मुख्य एसेट्स
        self.symbols = {
            'BTCUSDT': 'BITCOIN (BTC)',
            'ETHUSDT': 'ETHEREUM (ETH)',
            'SOLUSDT': 'SOLANA (SOL)',
            'PAXGUSDT': 'GOLD (PAXG)',
            'XAGUSDT': 'SILVER (XAG)'
        }

        self.asset_labels = {}

        # कार्ड्स बनाना
        for symbol, name in self.symbols.items():
            card = BoxLayout(
                orientation='vertical', 
                padding=[10, 5, 10, 5], 
                spacing=2
            )
            
            # एसेट का नाम
            name_label = Label(
                text=f"• {name} •", 
                font_size='15sp', 
                bold=True, 
                size_hint_y=0.4,
                color=(0.3, 0.7, 1, 1),
                halign='center',
                valign='center'
            )
            name_label.bind(size=name_label.setter('text_size'))

            # प्राइस और सिग्नल डिटेल्स
            data_label = Label(
                text="Loading Market Data...", 
                font_size='12sp', 
                size_hint_y=0.6,
                halign='center',
                valign='center'
            )
            data_label.bind(size=data_label.setter('text_size'))

            card.add_widget(name_label)
            card.add_widget(data_label)

            self.grid.add_widget(card)
            self.asset_labels[symbol] = data_label

        Clock.schedule_once(self.update_market_data, 1)
        Clock.schedule_interval(self.update_market_data, 10)

        return self.main_layout

    def update_market_data(self, dt):
        for symbol, name in self.symbols.items():
            try:
                url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1m&limit=50"
                candles = requests.get(url, timeout=5).json()

                if isinstance(candles, list) and len(candles) > 0:
                    high_prices = [float(c[2]) for c in candles]
                    low_prices = [float(c[3]) for c in candles]
                    close_prices = [float(c[4]) for c in candles]

                    current_price = close_prices[-1]
                    liquidity_high = max(high_prices[-25:-1])
                    liquidity_low = min(low_prices[-25:-1])

                    if current_price > liquidity_high:
                        signal = "BUY (BOS)"
                    elif current_price < liquidity_low:
                        signal = "SELL (BOS)"
                    else:
                        signal = "NEUTRAL"

                    display_text = (
                        f"Price: ${current_price:.2f} | Signal: {signal}\n"
                        f"Buy Liq: ${liquidity_high:.2f} | Sell Liq: ${liquidity_low:.2f}"
                    )
                    self.asset_labels[symbol].text = display_text

            except Exception:
                self.asset_labels[symbol].text = "Connecting..."

if __name__ == '__main__':
    SMCTradingApp().run()
