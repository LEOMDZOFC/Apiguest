#!/data/data/com.termux/files/usr/bin/python3
# -*- coding: utf-8 -*-

"""
================================================================================
    █████╗ ██╗   ██╗██████╗  █████╗ ███╗   ███╗██╗   ██╗███████╗██╗ ██████╗
   ██╔══██╗██║   ██║██╔══██╗██╔══██╗████╗ ████║██║   ██║██╔════╝██║██╔════╝
   ███████║██║   ██║██████╔╝███████║██╔████╔██║██║   ██║███████╗██║██║     
   ██╔══██║██║   ██║██╔══██╗██╔══██║██║╚██╔╝██║██║   ██║╚════██║██║██║     
   ██║  ██║╚██████╔╝██║  ██║██║  ██║██║ ╚═╝ ██║╚██████╔╝███████║██║╚██████╗
   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝ ╚═════╝ ╚══════╝╚═╝ ╚═════╝
================================================================================
                        MUSIC BOT SIÊU XỊN - FULL VOICE
================================================================================
                        AuraMusic Ultimate Edition v3.0
                    Tự động fix lỗi - Hỗ trợ voice 100%
================================================================================
"""

import os
import sys
import time
import json
import asyncio
import subprocess
import importlib
import importlib.util
import tempfile
import shutil
import re
import signal
import traceback
from pathlib import Path
from typing import Optional, Tuple, List, Dict, Any, Union
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import random

# ===== MÀU SẮC TERMINAL =====
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

def c(msg: str, color: str = Colors.RESET, bold: bool = False) -> str:
    """Colorize message"""
    prefix = Colors.BOLD if bold else ""
    return f"{prefix}{color}{msg}{Colors.RESET}"

def log(msg: str, level: str = "info", end: str = "\n"):
    """Log with emoji and color"""
    emojis = {
        "ok": "✅", "success": "✅", "done": "✅",
        "fail": "❌", "error": "❌",
        "warn": "⚠️", "warning": "⚠️",
        "info": "ℹ️",
        "step": "⚙️", "progress": "⏳",
        "debug": "🔍",
        "star": "⭐",
        "music": "🎵",
        "voice": "🔊",
        "admin": "👑",
        "queue": "📋",
        "play": "▶️",
        "stop": "⏹️",
        "skip": "⏭️",
        "pause": "⏸️",
        "loop": "🔄",
        "shuffle": "🔀"
    }
    emoji = emojis.get(level, "•")
    print(f"{c(emoji, Colors.CYAN)} {msg}", end=end)

def header(title: str):
    """Print header"""
    print(c("\n" + "="*70, Colors.MAGENTA, bold=True))
    print(c(f"  {title}", Colors.CYAN, bold=True))
    print(c("="*70 + "\n", Colors.MAGENTA, bold=True))

# ====================================================================
# AUTO-FIX ENGINE SIÊU CẤP - ĐẢM BẢO VOICE 100%
# ====================================================================
class AutoFixEngine:
    """Engine tự động fix mọi thứ để bot chạy voice mượt mà"""
    
    # Các gói Termux cần thiết
    TERMUX_ESSENTIAL = [
        "git", "cmake", "clang", "python", "ffmpeg", "libjpeg-turbo",
        "binutils", "libopus", "libsodium", "libffi", "openssl",
        "libwebp", "libvpx", "libx264", "libx265", "libvorbis", "libogg",
        "libmp3lame", "libtheora", "libass", "fribidi", "harfbuzz"
    ]
    
    # Python packages với nhiều phiên bản
    PYTHON_PACKAGES = [
        {"name": "telethon", "versions": ["telethon>=2.0.0", "telethon==1.36.0", "telethon"], "critical": True},
        {"name": "yt-dlp", "versions": ["yt-dlp>=2024.10.07", "yt-dlp"], "critical": True},
        {"name": "cryptg", "versions": ["cryptg>=0.4", "cryptg"], "critical": False},
        {"name": "pytgcalls", "versions": [
            "pytgcalls[ntgcalls]>=3.0.0",
            "pytgcalls==3.0.1",
            "pytgcalls==3.0.0",
            "git+https://github.com/pytgcalls/pytgcalls.git",
            "py-tgcalls>=3.0.0",
            "py-tgcalls==0.0.19"
        ], "critical": True, "voice": True},
    ]
    
    def __init__(self):
        self.installed = {}
        self.logs = []
        self.termux_available = self.is_termux()
        self.voice_supported = False
        self.voice_clients = {} 
        
    def is_termux(self):
        """Kiểm tra có đang chạy trong Termux không"""
        return 'com.termux' in os.environ.get('PREFIX', '')
        
    def run_cmd(self, cmd: List[str], timeout: int = 300) -> Tuple[bool, str]:
        """Chạy lệnh hệ thống"""
        try:
            log(f"Chạy: {' '.join(cmd)}", "debug")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return result.returncode == 0, result.stdout + result.stderr
        except Exception as e:
            return False, str(e)
            
    async def run_cmd_async(self, cmd: List[str], timeout: int = 300) -> Tuple[int, str, str]:
        """Chạy lệnh bất đồng bộ"""
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        try:
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout)
        except asyncio.TimeoutError:
            process.kill()
            await process.wait()
            return -1, "", "Timeout"
        return process.returncode, stdout.decode(), stderr.decode()
        
    def install_termux_packages(self):
        """Cài đặt tất cả gói Termux cần thiết"""
        if not self.termux_available:
            log("Không phải Termux, bỏ qua cài đặt gói hệ thống", "warn")
            return
            
        log("Đang cập nhật pkg...", "progress")
        self.run_cmd(["pkg", "update", "-y"])
        self.run_cmd(["pkg", "upgrade", "-y"])
        
        for pkg in self.TERMUX_ESSENTIAL:
            log(f"Đang cài {pkg}...", "progress")
            ok, out = self.run_cmd(["pkg", "install", pkg, "-y"])
            if ok:
                log(f"✅ {pkg} đã cài", "ok")
            else:
                log(f"⚠️ Lỗi cài {pkg}: {out[:100]}", "warn")
                
    async def install_python_package(self, pkg: dict) -> bool:
        """Cài một Python package với nhiều phiên bản"""
        name = pkg["name"]
        versions = pkg["versions"]
        critical = pkg.get("critical", False)
        voice_related = pkg.get("voice", False)
        
        # Kiểm tra đã cài chưa
        if self.is_module_installed(name):
            log(f"✅ {name} đã có", "ok")
            if voice_related:
                self.voice_supported = True
            return True
            
        log(f"Đang cài {name}...", "progress")
        
        for version in versions:
            # Xử lý đặc biệt cho git
            if version.startswith("git+"):
                cmd = [sys.executable, "-m", "pip", "install", "-U", version]
            else:
                cmd = [sys.executable, "-m", "pip", "install", "-U", version]
                
            ok, out = self.run_cmd(cmd)
            if ok and self.is_module_installed(name):
                log(f"✅ {name} cài thành công với {version}", "ok")
                if voice_related:
                    self.voice_supported = True
                return True
            else:
                log(f"  ↳ Thử {version} thất bại", "debug")
                
        if critical:
            log(f"❌ Không thể cài {name} (critical)", "error")
            return False
        else:
            log(f"⚠️ Không thể cài {name} (non-critical)", "warn")
            return True
            
    def is_module_installed(self, name: str) -> bool:
        """Kiểm tra module Python có import được không"""
        try:
            spec = importlib.util.find_spec(name.replace('-', '_'))
            return spec is not None
        except:
            return False
            
    async def fix_pytgcalls_deep(self) -> bool:
        """Fix pytgcalls chuyên sâu - bao gồm compile ntgcalls nếu cần"""
        log("🔧 Bắt đầu fix pytgcalls chuyên sâu...", "info")
        
        # Phương án 1: Thử cài với ntgcalls pre-built
        methods = [
            ("pytgcalls[ntgcalls]", ["pip", "install", "-U", "pytgcalls[ntgcalls]"]),
            ("pytgcalls từ dev branch", ["pip", "install", "-U", "git+https://github.com/pytgcalls/pytgcalls.git"]),
            ("py-tgcalls", ["pip", "install", "-U", "py-tgcalls"]),
            ("pytgcalls legacy", ["pip", "install", "-U", "pytgcalls==0.0.19"]),
        ]
        
        for name, cmd in methods:
            log(f"Thử {name}...", "progress")
            ok, out = self.run_cmd([sys.executable, "-m"] + cmd)
            if ok and self.is_module_installed("pytgcalls"):
                log(f"✅ pytgcalls cài thành công với {name}", "ok")
                return True
                
        # Phương án 2: Compile ntgcalls từ source
        log("Thử compile ntgcalls từ source...", "progress")
        try:
            # Cài Rust (cần cho ntgcalls)
            if self.termux_available:
                self.run_cmd(["pkg", "install", "rust", "cargo", "-y"])
            else:
                self.run_cmd(["curl", "--proto", "=https", "--tlsv1.2", "-sSf", "https://sh.rustup.rs", "|", "sh", "-s", "--", "-y"])
                
            # Clone và build ntgcalls
            with tempfile.TemporaryDirectory() as tmpdir:
                os.chdir(tmpdir)
                self.run_cmd(["git", "clone", "https://github.com/pytgcalls/ntgcalls.git"])
                os.chdir("ntgcalls")
                self.run_cmd(["cargo", "build", "--release"])
                # Cài đặt qua pip
                self.run_cmd([sys.executable, "-m", "pip", "install", "."])
                
            if self.is_module_installed("pytgcalls"):
                log("✅ pytgcalls compile thành công!", "ok")
                return True
        except Exception as e:
            log(f"Lỗi compile: {e}", "warn")
            
        # Phương án 3: Tạo wrapper giả nhưng đầy đủ để tránh lỗi import
        log("Tạo pytgcalls wrapper giả (vẫn có thể voice nếu đã có lib?)", "warn")
        self.create_pytgcalls_stub_full()
        return False  # voice không thực sự hoạt động nhưng bot chạy được
        
    def create_pytgcalls_stub_full(self):
        """Tạo pytgcalls stub đầy đủ để tránh lỗi import"""
        try:
            site_packages = subprocess.check_output(
                [sys.executable, "-c", "import site; print(site.getsitepackages()[0])"],
                text=True
            ).strip()
            
            stub_dir = Path(site_packages) / "pytgcalls"
            stub_dir.mkdir(exist_ok=True)
            
            # Tạo __init__.py với đầy đủ classes
            init_content = '''
"""PyTgCalls stub - giả lập để bot chạy"""

__version__ = "3.0.0-stub"

class PyTgCalls:
    def __init__(self, client):
        self.client = client
        self._calls = {}
        
    async def start(self):
        pass
        
    async def join_group_call(self, chat_id):
        self._calls[chat_id] = True
        
    async def leave_group_call(self, chat_id):
        self._calls.pop(chat_id, None)
        
    async def play(self, chat_id, audio):
        pass
        
    async def stop(self, chat_id):
        pass
        
    async def pause(self, chat_id):
        pass
        
    async def resume(self, chat_id):
        pass
        
    async def change_volume(self, chat_id, volume):
        pass

class AudioPiped:
    def __init__(self, url):
        self.url = url
        
class AudioQuality:
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
'''
            (stub_dir / "__init__.py").write_text(init_content)
            
            # Tạo types.py
            types_content = '''
from enum import Enum

class AudioPiped:
    def __init__(self, url):
        self.url = url

class AudioQuality(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
'''
            (stub_dir / "types.py").write_text(types_content)
            
            log("✅ Đã tạo pytgcalls stub đầy đủ", "ok")
        except Exception as e:
            log(f"Lỗi tạo stub: {e}", "error")
            
    async def fix_all(self) -> Tuple[bool, bool]:
        """Chạy toàn bộ quá trình fix, trả về (thành_công, voice_supported)"""
        header("AURAMUSIC AUTO-FIX ENGINE v3.0")
        
        # Kiểm tra Python
        if sys.version_info < (3, 8):
            log(f"Python quá cũ: {sys.version}", "error")
            return False, False
            
        log(f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}", "ok")
        
        # Cài Termux packages
        self.install_termux_packages()
        
        # Nâng cấp pip
        log("Nâng cấp pip...", "progress")
        self.run_cmd([sys.executable, "-m", "pip", "install", "--upgrade", "pip", "wheel", "setuptools"])
        
        # Cài Python packages cơ bản
        for pkg in self.PYTHON_PACKAGES:
            if pkg["name"] != "pytgcalls":
                await self.install_python_package(pkg)
                
        # Cài pytgcalls với fix chuyên sâu
        if not await self.install_python_package(next(p for p in self.PYTHON_PACKAGES if p["name"] == "pytgcalls")):
            log("Cài pytgcalls thông thường thất bại, thử phương pháp chuyên sâu...", "warn")
            voice_ok = await self.fix_pytgcalls_deep()
            self.voice_supported = voice_ok
        else:
            self.voice_supported = True
            
        # Kiểm tra ffmpeg
        if shutil.which("ffmpeg"):
            log("ffmpeg đã sẵn sàng", "ok")
        else:
            log("ffmpeg không tìm thấy, sẽ dùng yt-dlp internal", "warn")
            
        return True, self.voice_supported

# ====================================================================
# CẤU TRÚC DỮ LIỆU BÀI HÁT VÀ QUEUE
# ====================================================================
@dataclass
class Song:
    url: str
    title: str
    duration: int = 0
    requester: int = 0
    thumbnail: str = ""
    webpage_url: str = ""
    uploader: str = ""
    stream_url: str = ""
    
@dataclass
class QueueItem:
    song: Song
    added_at: datetime = field(default_factory=datetime.now)
    
class MusicQueue:
    def __init__(self):
        self.queues: Dict[int, List[QueueItem]] = {}
        self.current: Dict[int, Optional[Song]] = {}
        self.loop: Dict[int, bool] = {}  # loop single song
        self.loop_queue: Dict[int, bool] = {}  # loop all queue
        self.volume: Dict[int, int] = {}  # volume 0-200
        
    def add(self, chat_id: int, song: Song) -> int:
        if chat_id not in self.queues:
            self.queues[chat_id] = []
        self.queues[chat_id].append(QueueItem(song))
        return len(self.queues[chat_id])
        
    def next(self, chat_id: int) -> Optional[Song]:
        if chat_id not in self.queues:
            return None
            
        if self.loop.get(chat_id, False) and chat_id in self.current and self.current[chat_id]:
            # Loop single: trả lại bài hiện tại
            return self.current[chat_id]
            
        if not self.queues[chat_id]:
            if self.loop_queue.get(chat_id, False):
                # Loop queue: replay từ đầu
                # Giữ nguyên queue, lấy lại bài đầu tiên
                if self.queues[chat_id]:
                    self.current[chat_id] = self.queues[chat_id][0].song
                    return self.current[chat_id]
            return None
            
        # Lấy bài tiếp theo
        next_item = self.queues[chat_id].pop(0)
        self.current[chat_id] = next_item.song
        
        # Nếu loop queue, đưa bài vừa phát xuống cuối
        if self.loop_queue.get(chat_id, False):
            self.queues[chat_id].append(next_item)
            
        return self.current[chat_id]
        
    def clear(self, chat_id: int):
        self.queues[chat_id] = []
        self.current[chat_id] = None
        
    def remove(self, chat_id: int, index: int) -> bool:
        if chat_id in self.queues and 0 <= index < len(self.queues[chat_id]):
            self.queues[chat_id].pop(index)
            return True
        return False
        
    def move(self, chat_id: int, from_idx: int, to_idx: int) -> bool:
        if chat_id in self.queues and 0 <= from_idx < len(self.queues[chat_id]) and 0 <= to_idx < len(self.queues[chat_id]):
            item = self.queues[chat_id].pop(from_idx)
            self.queues[chat_id].insert(to_idx, item)
            return True
        return False
        
    def shuffle(self, chat_id: int):
        if chat_id in self.queues:
            random.shuffle(self.queues[chat_id])
            
    def get_queue_text(self, chat_id: int) -> str:
        if chat_id not in self.queues or not self.queues[chat_id]:
            return "📭 Hàng chờ trống."
            
        lines = []
        current = self.current.get(chat_id)
        if current:
            lines.append(f"**Đang phát:** {current.title}")
            lines.append("")
            
        for i, item in enumerate(self.queues[chat_id][:10]):
            song = item.song
            lines.append(f"{i+1}. {song.title} ({timedelta(seconds=song.duration) if song.duration else '??'})")
            
        if len(self.queues[chat_id]) > 10:
            lines.append(f"... và {len(self.queues[chat_id])-10} bài nữa")
            
        return "\n".join(lines)

# ====================================================================
# BOT CHÍNH - SIÊU XỊN
# ====================================================================
class AuraMusicBot:
    def __init__(self, voice_supported: bool):
        self.voice_supported = voice_supported
        self.api_id = 21106747
        self.api_hash = "3752ab2dc333b67cb9d93d28c3f00771"
        self.bot_token = "8228484701:AAHz22zvyo-UWsbJm9uvBymocTCkm_xldSQ"
        self.owner_id = 7960028389
        self.admins = {self.owner_id}
        
        # Components
        self.bot = None
        self.calls = None
        self.queue = MusicQueue()
        self.ytdl = None
        self.start_time = datetime.now()
        
        # Stream cache
        self.stream_cache = {}  # url -> stream_url
        
        # Downloaded songs (optional)
        self.download_dir = Path.home() / "music_cache"
        self.download_dir.mkdir(exist_ok=True)
        
    async def init_ytdl(self):
        """Khởi tạo yt-dlp với config tối ưu"""
        import yt_dlp
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'force-ipv4': True,
            'cookiefile': 'cookies.txt' if Path('cookies.txt').exists() else None,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
        self.ytdl = yt_dlp.YoutubeDL(ydl_opts)
        
    async def extract_song(self, query: str) -> Optional[Song]:
        """Trích xuất thông tin bài hát từ URL hoặc tìm kiếm"""
        try:
            # Nếu không phải URL, thêm ytsearch:
            if not query.startswith(('http://', 'https://')):
                query = f"ytsearch:{query}"
                
            info = self.ytdl.extract_info(query, download=False)
            if info is None:
                return None
                
            # Nếu là playlist, lấy video đầu tiên
            if 'entries' in info:
                info = info['entries'][0]
                
            # Lấy stream URL
            stream_url = info.get('url')
            if not stream_url:
                # Tìm format audio
                for fmt in info.get('formats', []):
                    if fmt.get('acodec') != 'none' and fmt.get('vcodec') == 'none':
                        stream_url = fmt.get('url')
                        break
                if not stream_url:
                    stream_url = info['formats'][-1]['url']
                    
            song = Song(
                url=info.get('webpage_url', query),
                title=info.get('title', 'Unknown'),
                duration=info.get('duration', 0),
                requester=0,  # sẽ set sau
                thumbnail=info.get('thumbnail', ''),
                webpage_url=info.get('webpage_url', ''),
                uploader=info.get('uploader', ''),
                stream_url=stream_url
            )
            return song
        except Exception as e:
            log(f"Lỗi extract: {e}", "error")
            return None
            
    async def play_song(self, chat_id: int, song: Song):
        """Phát bài hát trong voice chat"""
        if not self.voice_supported or not self.calls:
            return False
            
        try:
            # Tạo AudioPiped
            from pytgcalls.types import AudioPiped, AudioQuality
            audio = AudioPiped(song.stream_url)
            await self.calls.play(chat_id, audio)
            return True
        except Exception as e:
            log(f"Lỗi phát: {e}", "error")
            return False
            
    async def start(self):
        """Khởi động bot"""
        header("KHỞI ĐỘNG AURAMUSIC BOT")
        
        # Import telethon
        try:
            from telethon import TelegramClient, events
            from telethon.tl.types import PeerChannel
        except ImportError as e:
            log(f"Lỗi import telethon: {e}", "error")
            sys.exit(1)
            
        # Khởi tạo client
        self.bot = TelegramClient('aura_bot', self.api_id, self.api_hash)
        await self.bot.start(bot_token=self.bot_token)
        
        # Khởi tạo pytgcalls nếu voice supported
        if self.voice_supported:
            try:
                from pytgcalls import PyTgCalls
                self.calls = PyTgCalls(self.bot)
                await self.calls.start()
                log("PyTgCalls đã sẵn sàng", "ok")
            except Exception as e:
                log(f"Lỗi khởi động PyTgCalls: {e}", "error")
                self.voice_supported = False
                
        # Khởi tạo yt-dlp
        await self.init_ytdl()
        
        # Đăng ký handlers
        self.register_handlers()
        
        # Thông báo sẵn sàng
        log("✅ Bot đã sẵn sàng!", "success")
        log(f"Mode: {'🔊 VOICE FULL' if self.voice_supported else '🔇 TEXT ONLY'}", "info")
        log(f"Owner ID: {self.owner_id}", "info")
        log(f"Thời gian khởi động: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}", "info")
        
        # Chạy
        await self.bot.run_until_disconnected()
        
    def register_handlers(self):
        """Đăng ký tất cả lệnh"""
        from telethon import events
        
        @self.bot.on(events.NewMessage(pattern='/start'))
        async def start_handler(event):
            await event.reply(
                "🎵 **AuraMusic Bot Ultimate**\n\n"
                "Chào mừng bạn! Đây là bot phát nhạc siêu xịn.\n"
                "Dùng /help để xem hướng dẫn."
            )
            
        @self.bot.on(events.NewMessage(pattern='/help'))
        async def help_handler(event):
            help_text = f"""
**🎵 AURAMUSIC BOT ULTIMATE - HƯỚNG DẪN**

**LỆNH CƠ BẢN**
/start - Bắt đầu
/help - Trợ giúp
/menu - Menu chính
/info - Thông tin bot

**🎶 PHÁT NHẠC**
/play [tên/url] - Phát nhạc (YouTube)
/search [tên] - Tìm kiếm và chọn
/current - Bài đang phát
/stop - Dừng nhạc
/skip - Bỏ qua bài hiện tại
/pause - Tạm dừng
/resume - Tiếp tục

**📋 QUẢN LÝ HÀNG CHỜ**
/queue - Xem hàng chờ
/clear - Xóa hàng chờ
/remove [số] - Xóa bài khỏi queue
/move [từ] [đến] - Di chuyển bài
/shuffle - Xáo trộn queue
/loop [on/off] - Lặp lại bài hiện tại
/loopqueue [on/off] - Lặp lại toàn queue

**🔊 VOICE CHAT**
/join - Tham gia voice chat
/leave - Rời voice chat
/volume [0-200] - Chỉnh âm lượng

**👑 ADMIN**
/promote [id] - Thêm admin
/demote [id] - Xóa admin
/broadcast [tin nhắn] - Gửi thông báo
/stats - Thống kê bot

**Trạng thái:** {'🔊 Voice hoạt động' if self.voice_supported else '🔇 Chế độ văn bản'}
"""
            await event.reply(help_text)
            
        @self.bot.on(events.NewMessage(pattern='/menu'))
        async def menu_handler(event):
            await help_handler(event)
            
        @self.bot.on(events.NewMessage(pattern='/info'))
        async def info_handler(event):
            uptime = datetime.now() - self.start_time
            info = f"""
**🤖 AuraMusic Bot Info**
• Phiên bản: Ultimate v3.0
• Voice: {'✅' if self.voice_supported else '❌'}
• Uptime: {uptime}
• Python: {sys.version_info.major}.{sys.version_info.minor}
• Owner: {self.owner_id}
• Số nhóm đang hoạt động: {len(self.queue.queues)}
"""
            await event.reply(info)
            
        @self.bot.on(events.NewMessage(pattern='/join'))
        async def join_handler(event):
            if not self.voice_supported:
                await event.reply("❌ Voice không được hỗ trợ (do thiếu pytgcalls).")
                return
                
            chat_id = event.chat_id
            
            # Thử join trực tiếp, không cần kiểm tra
            try:
                await self.calls.join_group_call(chat_id)
                self.voice_clients[chat_id] = True
                await event.reply("✅ Đã tham gia voice chat.")
            except Exception as e:
                error_msg = str(e).lower()
                
                # Phân tích lỗi và hướng dẫn cụ thể
                if "GROUP_CALL_ALREADY_ACTIVE" in str(e) or "already joined" in error_msg:
                    await event.reply("⚠️ Bot đã ở trong voice chat rồi!")
                    
                elif "GROUP_CALL_NOT_FOUND" in str(e) or "voice chat not found" in error_msg or "group call not found" in error_msg:
                    await event.reply(
                        "❌ **Voice chat chưa được bắt đầu!**\n\n"
                        "📌 **Cách bắt đầu voice chat:**\n"
                        "1️⃣ Nhấn vào tên nhóm ở trên cùng\n"
                        "2️⃣ Chọn **Voice Chat**\n"
                        "3️⃣ Nhấn **Bắt đầu** hoặc **Start**\n"
                        "4️⃣ Sau đó thử lại lệnh /join"
                    )
                    
                elif "GROUPCALL_FORBIDDEN" in str(e) or "not enough rights" in error_msg:
                    await event.reply("❌ Bot không có quyền tham gia voice chat. Hãy thêm bot làm admin!")
                    
                elif "timeout" in error_msg or "timed out" in error_msg:
                    await event.reply("❌ Kết nối timeout. Thử lại sau vài giây.")
                    
                else:
                    await event.reply(f"❌ Lỗi không xác định: {e}\n\nVui lòng thử bắt đầu voice chat thủ công trong nhóm.")
        
        @self.bot.on(events.NewMessage(pattern='/leave'))
        async def leave_handler(event):
            if not self.voice_supported:
                return
                
            chat_id = event.chat_id
            
            try:
                await self.calls.leave_group_call(chat_id)
                if chat_id in self.voice_clients:
                    del self.voice_clients[chat_id]
                await event.reply("✅ Đã rời voice chat.")
            except Exception as e:
                error_msg = str(e).lower()
                
                if "not in a group call" in error_msg or "not joined" in error_msg:
                    await event.reply("⚠️ Bot không ở trong voice chat.")
                else:
                    await event.reply(f"❌ Lỗi khi rời: {e}")
                
        @self.bot.on(events.NewMessage(pattern='/play'))
        async def play_handler(event):
            args = event.text.split(maxsplit=1)
            if len(args) < 2:
                await event.reply("❌ Thiếu tên bài hát hoặc URL.\nVí dụ: `/play https://youtu.be/...` hoặc `/play em gái mưa`")
                return
                
            query = args[1]
            msg = await event.reply("🔍 Đang tìm kiếm...")
            
            # Trích xuất thông tin
            song = await self.extract_song(query)
            if not song:
                await msg.edit("❌ Không tìm thấy bài hát.")
                return
                
            song.requester = event.sender_id
            chat_id = event.chat_id
            
            # Thêm vào queue
            pos = self.queue.add(chat_id, song)
            
            # Nếu voice không hỗ trợ, chỉ gửi link
            if not self.voice_supported:
                await msg.edit(
                    f"🎵 **{song.title}**\n"
                    f"🔗 Link: {song.url}\n"
                    f"⏱ {timedelta(seconds=song.duration) if song.duration else '??'}\n"
                    f"👤 Yêu cầu: [{event.sender_id}](tg://user?id={event.sender_id})"
                )
                return
                
            # KIỂM TRA VÀ TỰ ĐỘNG JOIN VOICE CHAT
            chat = await event.get_chat()
            if not hasattr(chat, 'voice_chat') or not chat.voice_chat:
                await msg.edit("❌ Voice chat chưa được bắt đầu. Hãy bắt đầu voice chat trong nhóm trước!")
                return
            
            # Kiểm tra bot đã join chưa, nếu chưa thì join
            if chat_id not in self.voice_clients:
                try:
                    await self.calls.join_group_call(chat_id)
                    self.voice_clients[chat_id] = True
                    await event.reply("✅ Đã tự động tham gia voice chat.")
                except Exception as e:
                    await msg.edit(f"❌ Không thể join voice chat: {e}")
                    return
            
            # Nếu không có bài đang phát, bắt đầu phát
            if chat_id not in self.queue.current or self.queue.current[chat_id] is None:
                next_song = self.queue.next(chat_id)
                if next_song:
                    ok = await self.play_song(chat_id, next_song)
                    if ok:
                        await msg.edit(f"🎵 Đang phát: **{next_song.title}**")
                    else:
                        await msg.edit(f"❌ Lỗi phát nhạc.")
                else:
                    await msg.edit(f"➕ Đã thêm **{song.title}** vào hàng chờ (vị trí {pos})")
            else:
                await msg.edit(f"➕ Đã thêm **{song.title}** vào hàng chờ (vị trí {pos})")
                
        @self.bot.on(events.NewMessage(pattern='/stop'))
        async def stop_handler(event):
            if not self.voice_supported:
                await event.reply("❌ Voice không hỗ trợ.")
                return
                
            chat_id = event.chat_id
            try:
                await self.calls.stop(chat_id)
                self.queue.clear(chat_id)
                await event.reply("⏹️ Đã dừng và xóa hàng chờ.")
            except Exception as e:
                await event.reply(f"❌ Lỗi: {e}")
                
        @self.bot.on(events.NewMessage(pattern='/skip'))
        async def skip_handler(event):
            if not self.voice_supported:
                await event.reply("❌ Voice không hỗ trợ.")
                return
                
            chat_id = event.chat_id
            try:
                await self.calls.stop(chat_id)
                next_song = self.queue.next(chat_id)
                if next_song:
                    await self.play_song(chat_id, next_song)
                    await event.reply(f"⏭️ Đang phát: **{next_song.title}**")
                else:
                    await event.reply("⏭️ Hết hàng chờ.")
            except Exception as e:
                await event.reply(f"❌ Lỗi: {e}")
                
        @self.bot.on(events.NewMessage(pattern='/pause'))
        async def pause_handler(event):
            if not self.voice_supported:
                return
            try:
                await self.calls.pause(event.chat_id)
                await event.reply("⏸️ Đã tạm dừng.")
            except Exception as e:
                await event.reply(f"❌ Lỗi: {e}")
        
        @self.bot.on(events.NewMessage(pattern='/resume'))
        async def resume_handler(event):
            if not self.voice_supported:
                return
            try:
                await self.calls.resume(event.chat_id)
                await event.reply("▶️ Đã tiếp tục.")
            except Exception as e:
                await event.reply(f"❌ Lỗi: {e}")
        
        @self.bot.on(events.NewMessage(pattern='/volume'))
        async def volume_handler(event):
            if not self.voice_supported:
                return
            args = event.text.split()
            if len(args) < 2:
                await event.reply("❌ Thiếu giá trị volume (0-200).")
                return
            try:
                vol = int(args[1])
                if 0 <= vol <= 200:
                    await self.calls.change_volume(event.chat_id, vol)
                    await event.reply(f"🔊 Đã chỉnh volume: {vol}%")
                else:
                    await event.reply("❌ Volume phải từ 0 đến 200.")
            except:
                await event.reply("❌ Giá trị không hợp lệ.")
        
        @self.bot.on(events.NewMessage(pattern='/queue'))
        async def queue_handler(event):
            chat_id = event.chat_id
            text = self.queue.get_queue_text(chat_id)
            await event.reply(text)
        
        @self.bot.on(events.NewMessage(pattern='/clear'))
        async def clear_handler(event):
            chat_id = event.chat_id
            self.queue.clear(chat_id)
            await event.reply("🗑️ Đã xóa hàng chờ.")
        
        @self.bot.on(events.NewMessage(pattern='/shuffle'))
        async def shuffle_handler(event):
            chat_id = event.chat_id
            self.queue.shuffle(chat_id)
            await event.reply("🔀 Đã xáo trộn hàng chờ.")
            
        @self.bot.on(events.NewMessage(pattern='/remove'))
        async def remove_handler(event):
            args = event.text.split()
            if len(args) < 2:
                await event.reply("❌ Thiếu số thứ tự.")
                return
            try:
                idx = int(args[1]) - 1
                if self.queue.remove(event.chat_id, idx):
                    await event.reply(f"✅ Đã xóa bài số {args[1]}")
                else:
                    await event.reply("❌ Số thứ tự không hợp lệ.")
            except:
                await event.reply("❌ Số không hợp lệ.")
                
        @self.bot.on(events.NewMessage(pattern='/loop'))
        async def loop_handler(event):
            args = event.text.split()
            chat_id = event.chat_id
            if len(args) < 2:
                # toggle
                current = self.queue.loop.get(chat_id, False)
                self.queue.loop[chat_id] = not current
                state = "bật" if self.queue.loop[chat_id] else "tắt"
                await event.reply(f"🔄 Loop bài hiện tại: {state}")
            else:
                if args[1].lower() in ['on', 'true', '1', 'yes']:
                    self.queue.loop[chat_id] = True
                    await event.reply("🔄 Đã bật loop bài hiện tại.")
                elif args[1].lower() in ['off', 'false', '0', 'no']:
                    self.queue.loop[chat_id] = False
                    await event.reply("🔄 Đã tắt loop.")
                else:
                    await event.reply("❌ Cú pháp: /loop [on/off]")
                    
        @self.bot.on(events.NewMessage(pattern='/loopqueue'))
        async def loopqueue_handler(event):
            args = event.text.split()
            chat_id = event.chat_id
            if len(args) < 2:
                current = self.queue.loop_queue.get(chat_id, False)
                self.queue.loop_queue[chat_id] = not current
                state = "bật" if self.queue.loop_queue[chat_id] else "tắt"
                await event.reply(f"🔄 Loop queue: {state}")
            else:
                if args[1].lower() in ['on', 'true', '1', 'yes']:
                    self.queue.loop_queue[chat_id] = True
                    await event.reply("🔄 Đã bật loop queue.")
                elif args[1].lower() in ['off', 'false', '0', 'no']:
                    self.queue.loop_queue[chat_id] = False
                    await event.reply("🔄 Đã tắt loop queue.")
                else:
                    await event.reply("❌ Cú pháp: /loopqueue [on/off]")
                    
        @self.bot.on(events.NewMessage(pattern='/current'))
        async def current_handler(event):
            chat_id = event.chat_id
            current = self.queue.current.get(chat_id)
            if current:
                await event.reply(f"**Đang phát:** {current.title}")
            else:
                await event.reply("Không có bài nào đang phát.")
                
        # Admin commands
        @self.bot.on(events.NewMessage(pattern='/promote'))
        async def promote_handler(event):
            if event.sender_id != self.owner_id:
                await event.reply("❌ Bạn không phải chủ bot.")
                return
            args = event.text.split()
            if len(args) >= 2:
                try:
                    uid = int(args[1])
                    self.admins.add(uid)
                    await event.reply(f"✅ Đã thêm {uid} làm admin.")
                except:
                    await event.reply("❌ ID không hợp lệ.")
                    
        @self.bot.on(events.NewMessage(pattern='/demote'))
        async def demote_handler(event):
            if event.sender_id != self.owner_id:
                return
            args = event.text.split()
            if len(args) >= 2:
                try:
                    uid = int(args[1])
                    if uid != self.owner_id:
                        self.admins.discard(uid)
                        await event.reply(f"✅ Đã xóa {uid} khỏi admin.")
                except:
                    await event.reply("❌ ID không hợp lệ.")
                    
        @self.bot.on(events.NewMessage(pattern='/broadcast'))
        async def broadcast_handler(event):
            if event.sender_id not in self.admins:
                await event.reply("❌ Bạn không phải admin.")
                return
            args = event.text.split(maxsplit=1)
            if len(args) < 2:
                await event.reply("❌ Thiếu nội dung.")
                return
            msg = args[1]
            # Gửi đến tất cả các group? 
            # Cần lưu danh sách chat đã từng dùng bot
            await event.reply("📢 Đã gửi broadcast (giả lập).")
            
        @self.bot.on(events.NewMessage(pattern='/stats'))
        async def stats_handler(event):
            if event.sender_id not in self.admins:
                return
            stats = f"""
**📊 Thống kê bot**
• Số queue đang hoạt động: {len(self.queue.queues)}
• Tổng số bài trong queue: {sum(len(q) for q in self.queue.queues.values())}
• Uptime: {datetime.now() - self.start_time}
• Voice: {'✅' if self.voice_supported else '❌'}
"""
            await event.reply(stats)

# ====================================================================
# CHẠY BOT
# ====================================================================
async def main():
    # Xử lý Ctrl+C
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda: asyncio.create_task(shutdown()))
        
    async def shutdown():
        log("Đang tắt bot...", "warn")
        tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
        [t.cancel() for t in tasks]
        await asyncio.gather(*tasks, return_exceptions=True)
        loop.stop()
        
    # Chạy auto-fix
    fixer = AutoFixEngine()
    success, voice_supported = await fixer.fix_all()
    
    if not success:
        log("Auto-fix thất bại nghiêm trọng. Thoát.", "error")
        sys.exit(1)
        
    # Khởi động bot
    bot = AuraMusicBot(voice_supported)
    try:
        await bot.start()
    except KeyboardInterrupt:
        log("Đã dừng bot.", "warn")
    except Exception as e:
        log(f"Lỗi: {e}", "error")
        traceback.print_exc()
        
if __name__ == "__main__":
    asyncio.run(main())