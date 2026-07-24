import os
import sys
import time
import random
from dataclasses import dataclass
from collections import defaultdict
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.core.window import Window

# Set window size for desktop testing
Window.size = (500, 800)

# ─────────────────────────────────────────────
#  Data Structure — equivalent to C++ struct
# ─────────────────────────────────────────────

@dataclass
class Packet:
    src_ip: str
    dest_ip: str
    protocol: str
    size_bytes: int


# ─────────────────────────────────────────────
#  NetworkAnalyzer — equivalent to C++ class
# ─────────────────────────────────────────────

class NetworkAnalyzer:

    def __init__(self):
        self.total_packets_processed: int = 0
        self.total_bytes_processed: int = 0
        self.protocol_count: dict[str, int] = defaultdict(int)
        self.ip_traffic: dict[str, int] = defaultdict(int)

    def process_packet(self, pkt: Packet) -> None:
        """Analyse a new packet (process_packet in C++)"""
        self.total_packets_processed += 1
        self.total_bytes_processed += pkt.size_bytes
        self.protocol_count[pkt.protocol] += 1
        self.ip_traffic[pkt.src_ip] += pkt.size_bytes

    def get_dashboard_data(self) -> dict:
        """Return dashboard data as dictionary"""
        sorted_ips = sorted(self.ip_traffic.items(), key=lambda x: x[1], reverse=True)
        return {
            'total_packets': self.total_packets_processed,
            'total_kb': self.total_bytes_processed / 1024,
            'protocols': dict(self.protocol_count),
            'top_ips': sorted_ips[:5]
        }

    def reset(self) -> None:
        """Reset all statistics"""
        self.total_packets_processed = 0
        self.total_bytes_processed = 0
        self.protocol_count.clear()
        self.ip_traffic.clear()


# ─────────────────────────────────────────────
#  Random packet generator
# ─────────────────────────────────────────────

IPS = [
    "192.168.1.5",
    "10.0.0.12",
    "172.16.254.1",
    "192.168.1.20",
    "8.8.8.8",
]

PROTOCOLS = ["TCP", "UDP", "HTTP", "HTTPS", "DNS", "ICMP"]


def generate_random_packet() -> Packet:
    """Generate a random network packet"""
    src_ip = random.choice(IPS)
    dest_ip = random.choice(IPS)

    # Make sure source IP is different from destination IP
    while src_ip == dest_ip:
        dest_ip = random.choice(IPS)

    protocol = random.choice(PROTOCOLS)
    size_bytes = random.randint(40, 1500)

    return Packet(src_ip=src_ip, dest_ip=dest_ip,
                  protocol=protocol, size_bytes=size_bytes)


# ─────────────────────────────────────────────
#  Kivy GUI Application
# ─────────────────────────────────────────────

class NetworkAnalyzerApp(App):
    def build(self):
        self.analyzer = NetworkAnalyzer()
        self.is_running = False
        self.current_packet = None

        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Title
        title = Label(text='[b]Network Traffic Analyzer[/b]', 
                     markup=True, size_hint_y=0.08, font_size='20sp')
        main_layout.add_widget(title)

        # Dashboard area (scrollable)
        scroll_view = ScrollView(size_hint=(1, 0.65))
        self.dashboard_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.dashboard_layout.bind(minimum_height=self.dashboard_layout.setter('height'))
        scroll_view.add_widget(self.dashboard_layout)
        main_layout.add_widget(scroll_view)

        # Live packet info
        self.packet_label = Label(text='[i]Waiting for packets...[/i]', 
                                 markup=True, size_hint_y=0.15, font_size='12sp')
        main_layout.add_widget(self.packet_label)

        # Control buttons
        button_layout = BoxLayout(size_hint_y=0.12, spacing=10)
        
        self.start_btn = Button(text='Start', background_color=(0.2, 0.8, 0.2, 1))
        self.start_btn.bind(on_press=self.start_analysis)
        button_layout.add_widget(self.start_btn)

        self.stop_btn = Button(text='Stop', background_color=(0.8, 0.2, 0.2, 1))
        self.stop_btn.bind(on_press=self.stop_analysis)
        self.stop_btn.disabled = True
        button_layout.add_widget(self.stop_btn)

        self.reset_btn = Button(text='Reset', background_color=(0.2, 0.2, 0.8, 1))
        self.reset_btn.bind(on_press=self.reset_analysis)
        button_layout.add_widget(self.reset_btn)

        main_layout.add_widget(button_layout)

        # Start the update loop
        Clock.schedule_interval(self.update_dashboard, 0.1)

        return main_layout

    def start_analysis(self, instance):
        """Start analyzing packets"""
        self.is_running = True
        self.start_btn.disabled = True
        self.stop_btn.disabled = False

    def stop_analysis(self, instance):
        """Stop analyzing packets"""
        self.is_running = False
        self.start_btn.disabled = False
        self.stop_btn.disabled = True

    def reset_analysis(self, instance):
        """Reset all statistics"""
        self.is_running = False
        self.analyzer.reset()
        self.current_packet = None
        self.packet_label.text = '[i]Waiting for packets...[/i]'
        self.start_btn.disabled = False
        self.stop_btn.disabled = True
        self.refresh_dashboard()

    def update_dashboard(self, dt):
        """Update dashboard with new packet data"""
        if not self.is_running:
            return

        # Generate and process new packet
        self.current_packet = generate_random_packet()
        self.analyzer.process_packet(self.current_packet)

        # Update packet label
        self.packet_label.text = (
            f'[b]Live Stream[/b]\n'
            f'{self.current_packet.src_ip} → {self.current_packet.dest_ip}\n'
            f'[{self.current_packet.protocol}] ({self.current_packet.size_bytes} bytes)'
        )

        # Update dashboard
        self.refresh_dashboard()

    def refresh_dashboard(self):
        """Refresh the dashboard display"""
        self.dashboard_layout.clear_widgets()

        data = self.analyzer.get_dashboard_data()

        # Total stats
        stats_text = (
            f'[b]📊 Statistics[/b]\n'
            f'Total Packets: {data["total_packets"]}\n'
            f'Total Data: {data["total_kb"]:.2f} KB'
        )
        self.dashboard_layout.add_widget(Label(text=stats_text, markup=True, size_hint_y=None, height=80))

        # Protocol distribution
        protocol_text = '[b]🔄 Protocols[/b]\n'
        if data['protocols']:
            for proto, count in data['protocols'].items():
                protocol_text += f'{proto}: {count}\n'
        else:
            protocol_text += 'No data\n'
        self.dashboard_layout.add_widget(Label(text=protocol_text, markup=True, size_hint_y=None, height=100))

        # Top IPs
        ip_text = '[b]🌐 Top IPs[/b]\n'
        if data['top_ips']:
            for ip, bytes_sent in data['top_ips']:
                ip_text += f'{ip}: {bytes_sent/1024:.2f} KB\n'
        else:
            ip_text += 'No data\n'
        self.dashboard_layout.add_widget(Label(text=ip_text, markup=True, size_hint_y=None, height=120))


if __name__ == '__main__':
    random.seed()
    NetworkAnalyzerApp().run()
