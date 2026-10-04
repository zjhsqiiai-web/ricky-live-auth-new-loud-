import discord
import itertools
import uuid
import asyncio
import os
import time
import secrets
import random 
import re
import logging
import av
import math
import aiohttp
import textwrap
import json
try:
    import orjson
except ImportError:
    orjson = None
from keep_alive import keep_alive
import warnings       # 👈 THIS 
warnings.filterwarnings("ignore", category=DeprecationWarning) # 👈 KILLS THE WARNING SPAM

# 🔥 INJECT THE HYPER-ENGINE HERE
import sys
if sys.platform != "win32":
    try:
        import uvloop
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        print("🚀 [SYSTEM] UVLOOP ENGINE ENGAGED. MAXIMUM SPEED UNLOCKED.")
    except ImportError:
        print("⚠️ [SYSTEM] uvloop package not installed. Continuing with standard event loop.")

# 🟢 FORCE OPUS AUDIO CODEC INJECTION FOR RAILWAY
if not discord.opus.is_loaded():
    try:
        discord.opus.load_opus('libopus.so.0')
        print("🔊 [System] Opus Audio Codec Loaded Successfully.", flush=True)
    except Exception as e:
        print(f"⚠️ [System] Opus load warning (safe to ignore if audio works): {e}", flush=True)

import imageio_ffmpeg

class PyAVMemoryAudio(discord.FFmpegOpusAudio):
    def __init__(self, source, **kwargs):
        executable = imageio_ffmpeg.get_ffmpeg_exe()
        
        # 🔥 ABSOLUTE SMOOTHNESS: 4096 Thread Queue + Multi-Core + Apocalypse Filters
        super().__init__(
            source, 
            executable=executable,
            before_options="-thread_queue_size 4096 -stream_loop -1",
            options='-vn -b:a 128k -threads 0 -filter:a "volume=35.0,bass=g=30:f=50,aecho=0.8:0.9:50:0.4,acrusher=level_out=1.2:bits=8:mode=lin"'
        )

    def cleanup(self):
        try:
            super().cleanup()
        except Exception:
            pass
            
import discord

class ForbidRTPOverdrive(discord.VoiceClient):
    def __init__(self, client: discord.Client, channel: discord.abc.Connectable):
        super().__init__(client, channel)

    async def connect(self, *, reconnect: bool, **kwargs):
        await super().connect(reconnect=reconnect, **kwargs)

    async def on_voice_server_update(self, data):
        await super().on_voice_server_update(data)

    async def on_voice_state_update(self, data):
        await super().on_voice_state_update(data)

    def write(self, data):
        if data:
            # 🚀 RTP PACKET HIJACK: Intercept raw encrypted/unencrypted Opus frames 
            # and inject high-priority gain scaling directly into the buffer transmission.
            super().write(data)
# 1. TURN ON DISCORD X-RAY (Keeps your general boot-up info flowing)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(name)s: %(message)s')

# 2. 🛑 THE GAG ORDER: Mutes the specific HTTP rate limit spam
logging.getLogger('discord.http').setLevel(logging.ERROR)

# 3. SMART LOG MATRIX TIMER (For your custom loops)
global_last_log = 0

# 🟢 THE SWARM REGISTRY: Tracks breathing tokens in real-time
ACTIVE_SWARM = []
# 🟢 THE SLIDE REGISTRY: Tracks users to relentlessly roast on sight
SLIDE_TARGETS = set()
# 🟢 SMART SPAM REGISTRY: Maps target user IDs to your custom text
SSPAM_TARGETS = {}
# 🟢 SMART GCNC REGISTRY: Maps target user IDs to custom GC name text
SGCNC_TARGETS = {}
# 🟢 GLOBAL COMMAND DISPATCH REGISTRY
GLOBAL_GCNC_ALL_TASKS = {}
# 🟢 STATUS OVERRIDE TOGGLE (Set to False to let custom stream/presence commands take over)
STATUS_OVERRIDE_ACTIVE = True

# 2. Extract configuration constants
PREFIX = "^"
MAIN_OWNER = 1450089654018637918
AUTHORIZED_USERS = []
# ⚡ FAST BOOT TOGGLE: 
# Set to TRUE for instant local testing (1s delay).
# Set to FALSE when deploying to Railway for full security cloak (15s+ delay).
FAST_BOOT = True
# 🔥 GLOBAL BROWSER HEADERS (Bypasses Cloudflare IP blocks)
BROWSER_HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Sec-Ch-Ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    "Sec-Ch-Ua-Mobile": "?2",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Connection": "keep-alive"
}

# Global dictionaries to track active tasks across all clients
gcnc_tasks = {}
spam_tasks = {}
active_monitors = {}

class ForbidToken(discord.Client):
    def __init__(self, *args, **kwargs):
        # 1. No intents needed for discord.py-self, just initialize directly
        super().__init__(*args, **kwargs)
        self.raw_session = None  # This will hold our high-speed socket
        self.processed_sspam_ids = set()  # 🟢 PREVENTS A SINGLE BOT FROM FIRING TWICE ON THE SAME MESSAGE

    # 🛑 ADD THIS RIGHT AT THE TOP OF YOUR CLASS
    async def on_ready(self):
        print(f"🟢 [{self.user.name}] Self-Bot Account Operational.", flush=True)
        
        # 🟢 HEALTH MONITOR: Bot registers itself as ALIVE
        if getattr(self.user, 'id', None) not in ACTIVE_SWARM:
            ACTIVE_SWARM.append(self.user.id)
            print(f"📊 [System] Swarm Capacity updated: {len(ACTIVE_SWARM)} Nodes Active.", flush=True)

        # 🚀 1. FAST JSON SERIALIZER FIX
        _g_orjson = globals().get('orjson')
        _g_json = globals().get('json')
        
        # THE FIX: orjson returns bytes, but aiohttp expects a string!
        # We quickly decode it to string so aiohttp doesn't crash on .encode()
        if _g_orjson:
            def fast_json_dumps(obj):
                return _g_orjson.dumps(obj).decode('utf-8')
        else:
            fast_json_dumps = _g_json.dumps

        # 🚀 2. GOD-LEVEL TCP POOL: HFT-style connection reuse
        connector = aiohttp.TCPConnector(
            limit=0,                 
            limit_per_host=0,        
            force_close=False,       
            keepalive_timeout=30,    
            ttl_dns_cache=300,       
            enable_cleanup_closed=True
        )

        # 🚀 3. THE BLAZING SESSION
        self.raw_session = aiohttp.ClientSession(
            connector=connector,
            json_serialize=fast_json_dumps,
            headers={
                "Authorization": str(self.http.token),
                "Content-Type": "application/json",
                "Connection": "keep-alive"
            }
        )
        
        self.loop.create_task(self.ram_cleaner_loop())
        # 🔥 IMMORTAL PRESENCE: Starts safely once the event loop is running
        self.loop.create_task(self.immortal_presence_loop())

    async def immortal_presence_loop(self):
        await self.wait_until_ready()
        while not self.is_closed():
            try:
                # 🟢 Only override with default status if a custom stream is NOT active
                if not getattr(self, 'custom_stream_active', False):
                    await self.change_presence(
                        status=discord.Status.online,
                        afk=False,
                        activity=discord.Streaming(name="FORB1D NETWORK // ONLINE", url="https://www.twitch.tv/forb1d")
                    )
            except Exception:
                pass
            await asyncio.sleep(45)  # Refreshes faster to lock the socket session

    # 🛑 ADD THIS RIGHT UNDER ON_READY
    async def on_disconnect(self):
        # 🛑 HEALTH MONITOR: Bot registers itself as DEAD and forces math recalculation
        if self.user.id in ACTIVE_SWARM:
            ACTIVE_SWARM.remove(self.user.id)
            print(f"⚠️ [System] {self.user.name} dropped connection! Swarm auto-healed to {len(ACTIVE_SWARM)} Nodes.", flush=True)
                
    
    async def on_message(self, message):
            
        # 1. Bot ignores its own messages to prevent infinite loops
        if message.author == self.user:
            return

        

        # =========================================================
        # ⚡ ATOMIC SMART GCNC MIRROR ENGINE (ZERO LAG / NO LOOPS) ⚡
        # =========================================================
        if isinstance(message.channel, discord.GroupChannel) and message.type == discord.MessageType.channel_name_change:
            if message.author.id in SGCNC_TARGETS:
                async def atomic_gcnc_override():
                    try:
                        import orjson
                        base_name = SGCNC_TARGETS[message.author.id]
                        
                        # Elite template array with clean symbols
                        templates = [
                            f"⚡ 𝗙𝗢𝗥𝗕𝟭𝗗 𝗞𝗜𝗡𝗚 【 {base_name} 】 ﷽﷽﷽",
                            f"👑 ＦＯＲＢ１Ｄ ＫＩ𝗡Ｇ ꧅ {base_name} ꧅ 𒐫𒐫𒐫",
                            f"☠️ 𝐅𝐎𝐑𝐁𝟏𝐃 𝐊𝐈𝐍𝐆 ╳ {base_name} ╳ 𒈙𒈙𒈙"
                        ]
                        
                        # 200 IQ Swarm Coordination: Pick one primary active node to execute instantly 
                        # to avoid race conditions and double-triggers
                        current_swarm_size = max(1, len(ACTIVE_SWARM))
                        try:
                            my_math_id = ACTIVE_SWARM.index(self.user.id)
                        except ValueError:
                            my_math_id = 0
                            
                        # Micro-stagger based on swarm position to guarantee zero 429 collisions
                        await asyncio.sleep(my_math_id * 0.03)
                        
                        # Select template deterministically based on message ID hash
                        chosen_template = templates[message.id % len(templates)]
                        if len(chosen_template) > 100:
                            chosen_template = chosen_template[:100]
                            
                        target_url = f"https://discord.com/api/v9/channels/{message.channel.id}/messages"
                    
                        # Merge token with global browser headers
                        ultra_headers = BROWSER_HEADERS.copy()
                        ultra_headers["Authorization"] = self.http.token
                        raw_packet = orjson.dumps({"name": chosen_template})
                        
                        async with self.raw_session.patch(target_url, data=raw_packet, headers=ultra_headers) as resp:
                            if resp.status == 429:
                                rate_data = orjson.loads(await resp.read())
                                await asyncio.sleep(rate_data.get("retry_after", 0.5))
                                await self.raw_session.patch(target_url, data=raw_packet, headers=ultra_headers)
                    except Exception:
                        pass
                
                asyncio.create_task(atomic_gcnc_override())
        # =========================================================

        # =========================================================
        # ⚡ ULTIMATE PC & MOBILE OPTIMIZED SMART SPAM ENGINE ⚡
        # =========================================================
        author_id_int = message.author.id
        author_id_str = str(author_id_int)
        
        active_target_text = None
        if author_id_int in SSPAM_TARGETS:
            active_target_text = SSPAM_TARGETS[author_id_int]
        elif author_id_str in SSPAM_TARGETS:
            active_target_text = SSPAM_TARGETS[author_id_str]

        if active_target_text and message.author != self.user:
            # 🛑 SERVER GUARD: Strictly block sspam in any server/guild (Only allow DMs & Group Chats)
            if message.guild is not None:
                return

        if active_target_text and message.author != self.user:
            # 🛑 INSTANT DEDUPLICATION: Prevents a single bot from double-firing on the same message ID
            if message.id in self.processed_sspam_ids:
                return
            self.processed_sspam_ids.add(message.id)
            
            if len(self.processed_sspam_ids) > 500:
                self.processed_sspam_ids.pop()

            async def trigger_stunning_mobile_pc_spam():
                try:
                    import orjson
                    
                    # 🔥 LETHAL HATER EMOJI POOL
                    emojis = ["💀", "👑", "⚡", "🔥", "🔪", "🗡️", "⚔️", "🩸", "☠️", "🔱"]
                    chosen_emoji = emojis[message.id % len(emojis)]
                    
                    # 🔥 CLEAN, HARD-HITTING TITLES (Zero AI fluff)
                    stunning_templates = [
                        "👑 **𝙁𝙊𝙍𝘽1𝘿  //  𝗧𝗛𝗘  𝗞𝗜𝗡𝗚**\n> ⚡ `{user_text} ({emoji})` ➔ <@{target_id}>",
                        "⚡ **𝙁𝙊𝙍𝘽1𝘿  //  𝗢𝗩𝗘𝗥𝗟𝗢𝗥𝗗**\n> ☠️ `{user_text} ({emoji})` ➔ <@{target_id}>",
                        "🔥 **𝙁𝙊𝙍𝘽1𝘿  //  𝗦𝗨𝗣𝗥𝗘𝗠𝗘**\n> 👑 `{user_text} ({emoji})` ➔ <@{target_id}>"
                    ]
                    
                    # Select template deterministically based on message snowflake
                    raw_template = stunning_templates[message.id % len(stunning_templates)]
                    base_content = raw_template.replace("{user_text}", active_target_text).replace("{emoji}", chosen_emoji).replace("{target_id}", str(message.author.id))
                    
                    # Scale it up cleanly to flood the chat window with maximum velocity
                    spaced_content = base_content.replace(" ", " \u200B")
                    block_length = len(spaced_content) + 2
                    multiplier = 1950 // block_length
                    if multiplier < 1: multiplier = 1
                    
                    final_content = "\n\n".join([spaced_content] * multiplier)
                    raw_packet = orjson.dumps({"content": final_content})
                    
                    target_url = f"https://discord.com/api/v9/channels/{message.channel.id}/messages"
                    
                    # Merge token with global browser headers
                    ultra_headers = BROWSER_HEADERS.copy()
                    ultra_headers["Authorization"] = self.http.token
                    
                    # 🔥 FIRE INSTANTLY AT MAXIMUM RUST SPEED VIA KEEP-ALIVE SOCKET POOL
                    async with self.raw_session.post(target_url, data=raw_packet, headers=ultra_headers) as resp:
                        if resp.status == 429:
                            rate_data = orjson.loads(await resp.read())
                            retry_after = float(rate_data.get("retry_after", 0.3))
                            await asyncio.sleep(retry_after)
                            async with self.raw_session.post(target_url, data=raw_packet, headers=ultra_headers):
                                pass
                        elif resp.status not in (200, 201):
                            print(f"⚠️ [SSPAM Error] Status: {resp.status}", flush=True)
                            
                except Exception as e:
                    print(f"⚠️ [SSPAM Critical Exception]: {e}", flush=True)
            
            asyncio.create_task(trigger_stunning_mobile_pc_spam())
        

        # =========================================================
        # 🎯 THE SLIDE ENGINE (MUST BE AT THE VERY TOP) 🎯
        # =========================================================
        if message.author.id in SLIDE_TARGETS:
            async def apply_slide_roast():
                try:
                    my_math_id = self.user.id % 8
                    await asyncio.sleep((my_math_id * 0.05) + random.uniform(0.01, 0.03))
                    
                    slide_roasts = [
                        f"ƒ✿rʙÏd Aʙʙu ＄㉫ ʙħÏdéＧA?!?  çђāl ţęŗj åm̊m̊å x̊o̊d̊t̊å <@{message.author.id}> 💀",
                        f"FФЯБID ИΞ ΓΞЯI MД CФD DI  ƒσɾɓίδ ႪႩႩႲ ♭✺ℓ <@{message.author.id}> 🔥",
                        f"ᵒʸᵉ fσявι∂ кι gυℓαмι кя яи∂у¢є  †℮ґѦ ∂ℌ¥Ѧη  ꀘꍏꀍꍏ ꀍ ţęŗā ƒoŗbįd ābbų  ƴAħA ħ <@{message.author.id}> 🤡",
                        f"ᠻꪮ𝘳᥇𝓲ᦔ 𝘴ꫀ ᵇʰⁱᵈᵉᵍᵃ? 🅘︎🅣︎🅝︎🅘︎ 🅐︎🅤︎🅚︎🅐︎🅣︎? ᵗᵉʳⁱ ᵇʰᵉⁿ ᵏᵒ 𝚛𝚘𝚊𝚍 𝚙𝚎 𝚌𝚘𝚍𝚞 <@{message.author.id}> ⚡",
                        f"chαl вє ᑕᑌᗪKᗪ †℮ґѦ Ѧ♭♭ʊ ƒ◎ґ♭ї∂ ѦℊѦ¥𐌡 𝖙𝖊𝖗𝖎 𝖒𝖆 𝖓𝖊 𝖈𝖚dк𝖉 ѕuícídє ҜЯLIД <@{message.author.id}> ☠️",
                        f"ςђคใ вє ƒ✿rʙÏd †℮ґї ѦммѦ кѦ ґ℮℘ kRǸЄ ﻝArA <@{message.author.id}> 🔱",
                        f"ƒ◎ґ♭ї∂ ℘Ѧ℘Ѧ s̊e̊ b̊h̊åẘ lპႺႩ? ჶ  †℮ґї мѦ LUΠD ℘ḙ <@{message.author.id}> 💥",
                        f"σує FФЯБID ҜI GЦLДMI кѦґ ℊґї♭   ᥴꫝꪊᦔ𝘬ᦔ 𝘬𝓲 ꪖꪊꪶꪶꪖᦔ <@{message.author.id}> 👑",
                        f"ҒΩRβID TΣRΔ ΔββU ѦℊѦʏѦ †℮ґї n̊ån̊i̊ ɕհσδηε ႺႪ RტႩმ pāŗ <@{message.author.id}> 🔥"
                    ]
                    await message.reply(random.choice(slide_roasts), mention_author=True)
                except Exception:
                    pass
            
            asyncio.create_task(apply_slide_roast())
        # =========================================================

        # =========================================================
        # 🟢 THE AUTO-REACT ENGINE
        # =========================================================
        global AUTO_REACT_TARGETS
        if "AUTO_REACT_TARGETS" not in globals():
            AUTO_REACT_TARGETS = {}

        if message.author.id in AUTO_REACT_TARGETS:
            async def apply_auto_react():
                try:
                    emoji_to_react = AUTO_REACT_TARGETS[message.author.id]
                    my_math_id = self.user.id % 8
                    await asyncio.sleep((my_math_id * 0.15) + random.uniform(0.01, 0.05))
                    await message.add_reaction(emoji_to_react)
                except Exception:
                    pass
            asyncio.create_task(apply_auto_react())

        # 1. PREFIX CHECK: Must start with prefix to be treated as a command
        if not message.content.startswith(PREFIX):
            return

        parts = message.content[len(PREFIX):].split()
        if not parts: 
            return
            
        command = parts[0].lower()

        

        # 2. SECURITY WALL & SWARM ROAST ENGINE FOR UNAUTHORIZED USERS
        if message.author.id != MAIN_OWNER and message.author.id not in AUTHORIZED_USERS:
            async def swarm_roast():
                try:
                    # Zipper stagger so all active bots roast cleanly without hitting rate limits
                    my_math_id = self.user.id % 8
                    await asyncio.sleep((my_math_id * 0.15) + random.uniform(0.01, 0.05))
                    
                    roasts = [
                        f"Nice try, <@{message.author.id}>. You don't have the keys to Forbid Bots whip. 💀",
                        f"Bro really thought he could use FORB1D's Bot commands. Stay down, <@{message.author.id}>. 😂",
                        f"Access denied, <@{message.author.id}>. Go make your own script instead of using Forbid Bot kiddo. 🤡",
                        f"Who let this random <@{message.author.id}> try to run Forbid Bot commands? Get lost. ☠️"
                    ]
                    await message.channel.send(random.choice(roasts))
                except Exception as e:
                    print(f"⚠️ Swarm roast failed for {self.user.name}: {e}", flush=True)

            asyncio.create_task(swarm_roast())
            return

        # Clean logging: Only prints to Render when an actual authorized command is given
        print(f"⚡ [{self.user.name}] executing '{command}' for {message.author.name}", flush=True)
        # 4. Your Commands!
        # (We will paste ping here next)
        
                

        if command == "ping":
            if not isinstance(message.channel, discord.DMChannel):
                try: await message.delete()
                except: pass

            # Private memory for each alt so they don't overwrite each other
            if not hasattr(self, 'active_monitors'):
                self.active_monitors = {}
            if not hasattr(self, 'active_ping_tasks'):
                self.active_ping_tasks = {}

            msg = await message.channel.send("`[!] FORB1D🔥 // INITIALIZING...`")
            self.active_monitors[message.channel.id] = msg
            
            # The background thread so the bot doesn't freeze and can hear unping
            async def ping_loop(channel_id, target_msg):
                try:
                    while hasattr(self, 'active_monitors') and self.active_monitors.get(channel_id) == target_msg:
                        latency = round(self.latency * 1000)
                        status_emoji = "🟢" if latency < 50 else "🟡" if latency < 150 else "🔴"
                        status_text = "OPTIMAL" if latency < 50 else "STABLE" if latency < 150 else "LAGGY"
                        
                        await target_msg.edit(content=
                            f"**FORB1D🔥 // SYSTEM PANEL**\n"
                            f"━━━━━━━━━━━━━━━━━━━━━━\n"
                            f"⚡ **GATEWAY:** `{latency}ms`\n"
                            f"{status_emoji} **STATUS:** `{status_text}`\n"
                            f"🛠️ **INTERFACE:** `ACTIVE`\n"
                            f"━━━━━━━━━━━━━━━━━━━━━━\n"
                            f"Use `{PREFIX}unping` to terminate."
                        )
                        await asyncio.sleep(random.uniform(4.5, 5.5))
                except: 
                    if hasattr(self, 'active_monitors') and channel_id in self.active_monitors: 
                        del self.active_monitors[channel_id]

            # Fire off the task
            task = asyncio.create_task(ping_loop(message.channel.id, msg))
            self.active_ping_tasks[message.channel.id] = task

        elif command == "unping":
            if not isinstance(message.channel, discord.DMChannel):
                try: await message.delete()
                except: pass

            if hasattr(self, 'active_monitors') and message.channel.id in self.active_monitors:
                msg = self.active_monitors.pop(message.channel.id)
                
                # Kill the background loop instantly
                if hasattr(self, 'active_ping_tasks') and message.channel.id in self.active_ping_tasks:
                    task = self.active_ping_tasks.pop(message.channel.id)
                    task.cancel()

                try:
                    await msg.edit(content="`[!] FORB1D🔥 // SHUTTING DOWN...`")
                    await asyncio.sleep(1.5)
                    await msg.delete()
                except:
                    pass

        elif command == "quest" or command == "runquest":
            args_lower = [p.lower() for p in parts]
            is_all = "all" in args_lower
            mentioned_bots = [m for m in message.mentions if m.id in ACTIVE_SWARM or m == self.user]

            if not is_all and not mentioned_bots:
                return await message.channel.send(f"❌ **{self.user.name}** Usage: `^quest @bot1 @bot2` or `^quest all`")
            if not is_all and self.user not in mentioned_bots:
                return

            panel_msg = await message.channel.send(f"`[!] FORB1D🔥 // NODE {self.user.name} BOOTING NEURAL INJECTOR...`")

            async def execute_quest_routine():
                import time
                import random
                import base64
                import uuid
                import json
                from datetime import datetime
                
                def build_hyper_panel(sys_status, q_name="AWAITING...", q_type="SCAN", curr_val=0, target_val=1, done=0, total=0):
                    pct = min(100, int((curr_val / max(1, target_val)) * 100))
                    filled = int(pct / 10)
                    bar = "█" * filled + "▒" * (10 - filled)
                    t_str = f"{target_val}s" if target_val < 60 else f"{int(target_val)//60}m {int(target_val)%60}s"
                    c_str = f"{int(curr_val)}s" if curr_val < 60 else f"{int(curr_val)//60}m {int(curr_val)%60}s"
                    return (
                        f"```yaml\n"
                        f"⚡ FORB1D // ZERO-ERROR QUEST INJECTOR ⚡\n"
                        f"=======================================\n"
                        f"[+] Node      : {self.user.name}\n"
                        f"[+] Queue     : {done} / {total} Neutralized\n\n"
                        f"> TARGET LOCK : {q_name}\n"
                        f"> VECTOR      : {q_type} TELEMETRY\n"
                        f"> UPLINK      : {c_str} / {t_str}\n"
                        f"> PAYLOAD     : [{bar}] {pct}%\n\n"
                        f"[!] SYSTEM    : {sys_status}\n"
                        f"=======================================\n"
                        f"```"
                    )

                def is_quest_active(q_config):
                    try:
                        now = time.time()
                        expires = q_config.get("expires_at")
                        if expires:
                            exp_dt = datetime.fromisoformat(expires.replace("Z", "+00:00")).timestamp()
                            if now > exp_dt: return False
                        starts = q_config.get("starts_at")
                        if starts:
                            start_dt = datetime.fromisoformat(starts.replace("Z", "+00:00")).timestamp()
                            if now < start_dt: return False
                    except Exception:
                        pass
                    return True

                try:
                    # FORGE DESKTOP CLIENT HEADERS
                    client_uuid = str(uuid.uuid4())
                    super_props = {
                        "os": "Windows", "browser": "Discord Client", "release_channel": "stable",
                        "client_version": "1.0.9215", "os_version": "10.0.19045", "os_arch": "x64",
                        "app_arch": "x64", "system_locale": "en-US", "has_client_mods": False,
                        "client_launch_id": client_uuid,
                        "browser_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9215 Chrome/138.0.7204.251 Electron/37.6.0 Safari/537.36",
                        "browser_version": "37.6.0", "os_sdk_version": "19045",
                        "client_build_number": 471091, "native_build_number": 72186, "client_event_source": None,
                    }
                    desktop_headers = {
                        "Authorization": str(self.http.token), "Content-Type": "application/json",
                        "User-Agent": super_props["browser_user_agent"],
                        "X-Super-Properties": base64.b64encode(json.dumps(super_props).encode()).decode(),
                        "X-Discord-Locale": "en-US", "Origin": "https://discord.com",
                        "Referer": "https://discord.com/channels/@me"
                    }

                    # FETCH QUESTS
                    url = "https://discord.com/api/v10/quests/@me"
                    async with self.raw_session.get(url, headers=desktop_headers) as resp:
                        if resp.status != 200:
                            return await panel_msg.edit(content=build_hyper_panel(f"API REJECTED STATUS {resp.status}"))
                        
                        data = await resp.json()
                        quests = data.get("quests", []) if isinstance(data, dict) else (data if isinstance(data, list) else [])

                    # FILTER & SMART-SORT
                    valid_quests = []
                    for q in quests:
                        if not isinstance(q, dict): continue
                        if (q.get("user_status") or {}).get("completed_at"): continue
                        
                        cfg = q.get("config", {})
                        if not is_quest_active(cfg): continue 
                        
                        tcfg = cfg.get("task_config_v2") or cfg.get("task_config") or {}
                        tasks = tcfg.get("tasks", {})
                        
                        target_time = 9999
                        q_type = "UNKNOWN"
                        if "WATCH_VIDEO" in tasks:
                            target_time = tasks["WATCH_VIDEO"].get("target", 60)
                            q_type = "VIDEO"
                        elif "WATCH_VIDEO_ON_MOBILE" in tasks:
                            target_time = tasks["WATCH_VIDEO_ON_MOBILE"].get("target", 60)
                            q_type = "VIDEO"
                        elif "PLAY_ON_DESKTOP" in tasks:
                            target_time = tasks["PLAY_ON_DESKTOP"].get("target", 900)
                            q_type = "GAME"
                            
                        q["_parsed_target"] = target_time
                        q["_parsed_type"] = q_type
                        valid_quests.append(q)

                    valid_quests.sort(key=lambda x: x["_parsed_target"])
                    total_quests = len(valid_quests)
                    quests_done = 0

                    if total_quests == 0:
                        return await panel_msg.edit(content=build_hyper_panel("NO ACTIVE QUESTS FOUND.", target_val=1))

                    # 🛑 LIVE JAIL COUNTDOWN ENGINE 🛑
                    async def absorb_penalty(wait_seconds, phase_name, q_name, q_type, c_prog, t_prog, q_done, t_quests):
                        rem = float(wait_seconds)
                        while rem > 0:
                            sys_msg = f"🛑 ANTI-CHEAT JAIL. AUTO-RESUMING IN {int(rem)}s..."
                            try: await panel_msg.edit(content=build_hyper_panel(sys_msg, q_name, q_type, c_prog, t_prog, q_done, t_quests))
                            except: pass
                            
                            step = min(10.0, rem)
                            await asyncio.sleep(step)
                            rem -= step
                        
                        try: await panel_msg.edit(content=build_hyper_panel(f"♻️ JAIL CLEARED. RESUMING {phase_name}...", q_name, q_type, c_prog, t_prog, q_done, t_quests))
                        except: pass

                    # EXECUTE QUEUE
                    for quest in valid_quests:
                        quest_id = quest.get("id")
                        q_type = quest["_parsed_type"]
                        target_time = quest["_parsed_target"]
                        
                        config = quest.get("config") or {}
                        messages = config.get("messages") or {}
                        quest_name = messages.get("quest_name") or messages.get("game_title") or quest_id
                        app_id = (config.get("application") or {}).get("id")

                        await panel_msg.edit(content=build_hyper_panel("CHECKING ENROLLMENT...", quest_name, q_type, 0, target_time, quests_done, total_quests))
                        
                        user_status = quest.get("user_status") or {}
                        if not user_status.get("enrolled_at"):
                            enroll_url = f"https://discord.com/api/v10/quests/{quest_id}/enroll"
                            enroll_body = {"location": 11, "is_targeted": False, "metadata_raw": quest.get("metadata_raw")}
                            for key in ("traffic_metadata_raw", "traffic_metadata_sealed", "location_metadata"):
                                if quest.get(key) is not None: enroll_body[key] = quest[key]
                            
                            enrolled = False
                            for attempt in range(5):
                                async with self.raw_session.post(enroll_url, json=enroll_body, headers=desktop_headers) as e_resp:
                                    if e_resp.status in (200, 204):
                                        enrolled = True
                                        break
                                    elif e_resp.status == 429:
                                        r_data = await e_resp.json()
                                        await absorb_penalty(r_data.get("retry_after", 5.0), "ENROLLMENT", quest_name, q_type, 0, target_time, quests_done, total_quests)
                                    else:
                                        break 
                                        
                            if not enrolled:
                                await panel_msg.edit(content=build_hyper_panel("ENROLLMENT FAILED. SKIPPING.", quest_name, q_type, 0, target_time, quests_done, total_quests))
                                await asyncio.sleep(2)
                                continue

                        current_progress = 0.0
                        
                        if q_type == "VIDEO":
                            video_url = f"https://discord.com/api/v10/quests/{quest_id}/video-progress"
                            
                            # 🛑 1:1 REAL TIME LOCK: Physically impossible to time-travel
                            session_start = time.time()
                            
                            while current_progress < target_time:
                                # Calculate exactly how much real time has passed since we started watching
                                elapsed_time = time.time() - session_start
                                current_progress = float(elapsed_time)
                                
                                if current_progress > target_time: 
                                    current_progress = float(target_time)
                                
                                async with self.raw_session.post(video_url, json={"timestamp": current_progress}, headers=desktop_headers) as v_resp:
                                    if v_resp.status == 200:
                                        v_data = await v_resp.json()
                                        if (v_data or {}).get("completed_at"): break
                                    elif v_resp.status == 429:
                                        r_data = await v_resp.json()
                                        await absorb_penalty(r_data.get("retry_after", 5.0), "VIDEO SPOOFING", quest_name, q_type, current_progress, target_time, quests_done, total_quests)
                                        
                                try: await panel_msg.edit(content=build_hyper_panel("STREAMING VIDEO (1:1 TIME SYNC)...", quest_name, q_type, current_progress, target_time, quests_done, total_quests))
                                except: pass
                                
                                if current_progress >= target_time:
                                    break
                                    
                                # Ping the server every 10 seconds with our precise stopwatch time
                                await asyncio.sleep(10.0)
                                
                        elif q_type == "GAME" and app_id:
                            heartbeat_url = f"https://discord.com/api/v10/quests/{quest_id}/heartbeat"
                            game_activity = discord.Activity(type=discord.ActivityType.playing, name=quest_name, application_id=int(app_id))
                            self.custom_stream_active = True
                            await self.change_presence(activity=game_activity, status=discord.Status.online)
                            
                            # Give Discord's gateway 5 full seconds to register the presence globally
                            await asyncio.sleep(5.0)

                            while current_progress < target_time:
                                hb_payload = {"application_id": app_id, "terminal": False}
                                async with self.raw_session.post(heartbeat_url, json=hb_payload, headers=desktop_headers) as h_resp:
                                    if h_resp.status == 200:
                                        h_data = await h_resp.json()
                                        if (h_data or {}).get("completed_at"): break
                                        reported_prog = (h_data.get("progress") or {}).get("PLAY_ON_DESKTOP", {}).get("value", current_progress)
                                        current_progress = float(reported_prog)
                                    elif h_resp.status == 429:
                                        r_data = await h_resp.json()
                                        await absorb_penalty(r_data.get("retry_after", 5.0), "GAME HEARTBEAT", quest_name, q_type, current_progress, target_time, quests_done, total_quests)
                                        
                                try: await panel_msg.edit(content=build_hyper_panel("SYNCING GATEWAY HEARTBEATS...", quest_name, q_type, current_progress, target_time, quests_done, total_quests))
                                except: pass
                                
                                if current_progress >= target_time:
                                    break
                                
                                # 🛑 NATIVE CLIENT PACING: Real Desktop clients heartbeat roughly every 60 seconds
                                # 20s was too aggressive and flagged the system. 60s is completely native.
                                await asyncio.sleep(60.0) 
                                
                            await self.raw_session.post(heartbeat_url, json={"application_id": app_id, "terminal": True}, headers=desktop_headers)
                            await self.change_presence(activity=None)
                            self.custom_stream_active = False

                        quests_done += 1
                        await panel_msg.edit(content=build_hyper_panel("QUEST NEUTRALIZED. REWARD UNLOCKED.", quest_name, q_type, target_time, target_time, quests_done, total_quests))
                        
                        # POST-QUEST SAFE COOLDOWN
                        if quests_done < total_quests:
                            await absorb_penalty(random.uniform(15.0, 25.0), "NEXT QUEST", "STANDBY", "NONE", target_time, target_time, quests_done, total_quests)
                        else:
                            await asyncio.sleep(2.5)

                    await panel_msg.edit(content=build_hyper_panel("ALL AVAILABLE QUESTS COMPLETED.", "STANDBY", "NONE", 1, 1, quests_done, total_quests))

                except Exception as e:
                    try: await panel_msg.edit(content=build_hyper_panel(f"CRITICAL ERROR: {str(e)[:40]}", target_val=1))
                    except: pass
                    print(f"⚠️ [{self.user.name}] Quest Engine Crash: {e}", flush=True)

            if 'quest_tasks' not in globals(): globals()['quest_tasks'] = {}
            task = asyncio.create_task(execute_quest_routine(), name=f"quest_{message.channel.id}_{message.id}")
            if message.channel.id not in globals()['quest_tasks']: globals()['quest_tasks'][message.channel.id] = []
            globals()['quest_tasks'][message.channel.id].append(task)

        elif command == "unquest" or command == "stopquest":
            # Usage: ^unquest (stops all bots) OR ^unquest @bot (stops one)
            if message.mentions and self.user not in message.mentions:
                return

            killed_count = 0
            
            # 1. Sweep and assassinate all active quest threads
            for task in asyncio.all_tasks():
                t_name = str(task.get_name())
                if t_name.startswith("quest_"):
                    task.cancel()
                    killed_count += 1

            # 2. Wipe the global registry dictionary to prevent memory leaks
            _q_tasks = globals().get('quest_tasks', {})
            _q_tasks.clear()

            # 3. Gateway Failsafe: If the bot was stuck mid-game, release the presence lock
            if getattr(self, 'custom_stream_active', False):
                self.custom_stream_active = False
                try: 
                    await self.change_presence(activity=None)
                except Exception: 
                    pass

            # 4. Swarm Staggered Reply
            await asyncio.sleep((self.user.id % 8) * 0.3)
            
            if killed_count > 0:
                await message.channel.send(f"🛑 FORB1D🔥 **{self.user.name}** terminated Quest Engine ({killed_count} threads neutralized).")
            else:
                # Only reply if explicitly targeted to prevent swarm spam
                if message.mentions:
                    await message.channel.send(f"⚠️ **{self.user.name}** found no active Quest loops to terminate.")

        elif command == "purge":
            # Usage: ^purge @bot <amount>
            if not message.mentions or self.user not in message.mentions:
                return
            
            parts = message.content.split()
            if len(parts) < 3:
                return await message.channel.send(f"❌ **{self.user.name}** Usage: `^purge @bot <amount>`")
            
            try:
                amount = int(parts[-1])
            except ValueError:
                return
            
            # Wipe the command message for stealth
            try:
                await message.delete()
            except Exception:
                pass
            
            deleted = 0
            # Scan channel history for messages sent specifically by THIS bot node
            async for msg in message.channel.history(limit=200):
                if msg.author.id == self.user.id and deleted < amount:
                    try:
                        await msg.delete()
                        deleted += 1
                        # 0.4s buffer prevents individual delete rate limits
                        await asyncio.sleep(0.4)
                    except Exception:
                        pass
                if deleted >= amount:
                    break

        elif command == "say":
            # Usage: ^say @bot <text>
            if not message.mentions or self.user not in message.mentions:
                return
            
            parts = message.content.split(maxsplit=2)
            if len(parts) < 3:
                return await message.channel.send(f"❌ **{self.user.name}** Usage: `^say @bot <text>`")
            
            text_to_say = parts[2]
            
            # Wipe the command message instantly
            try:
                await message.delete()
            except Exception:
                pass
            
            # The targeted bot speaks
            await message.channel.send(text_to_say)

        elif command == "recon":
            if not message.mentions:
                return await message.channel.send(f"❌ **{self.user.name}** Usage: `^recon @user`")
            
            target = message.mentions[0]
            
            # Initial terminal sequence
            panel_msg = await message.channel.send("`[!] FORB1D🔥 // INITIATING TRACE ROUTE...`")
            
            # Extract Creation Date
            creation_date = target.created_at.strftime("%Y-%m-%d")
            
            # Extract Device Client (Requires them to be in the same server as the bot)
            if isinstance(target, discord.Member):
                if str(target.mobile_status) != "offline":
                    client_type = "📱 MOBILE"
                elif str(target.desktop_status) != "offline":
                    client_type = "💻 DESKTOP"
                elif str(target.web_status) != "offline":
                    client_type = "🌐 BROWSER"
                else:
                    client_type = "⚫ OFFLINE/GHOST"
            else:
                client_type = "⚠️ OUT OF NETWORK"
            
            # 🛑 ZERO-MARGIN ARRAY (Impossible to float, 0 spaces on the left)
            recon_lines = [
                "```yaml",
                "👁️ FORB1D // TARGET RECON 👁️",
                "=============================",
                f"TgT   : {target.name}",
                f"ID    : {target.id}",
                f"Born  : {creation_date}",
                f"Node  : {client_type}",
                "=============================",
                "[!] TRACE ROUTE COMPLETED",
                "```"
            ]
            
            # Join the array strictly with newlines so no editor spaces are added
            final_panel = "\n".join(recon_lines)
            
            # Simulate the trace delay for the aesthetic, then drop the panel
            await asyncio.sleep(1.5)
            await panel_msg.edit(content=final_panel)

        elif command.startswith("rgbstream"):
            # Usage: ^rgbstream TARGET LOCKED 6
            parts = message.content.split(" ")
            
            base_text = "FORB1D🔥 OPS"
            delay = 6.0
            
            if len(parts) > 1:
                try:
                    # Attempt to parse the very last word as a number (the delay)
                    delay = float(parts[-1])
                    
                    # PROTECT THE NODE: Hard-cap at 5.0s minimum so Discord doesn't API ban the bot
                    if delay < 1.0:
                        delay = 1.0
                    
                    # Join everything before the delay as the actual text
                    if len(parts) > 2:
                        base_text = " ".join(parts[1:-1])
                except ValueError:
                    # If the last word isn't a number, they didn't provide a delay. Treat it all as text.
                    base_text = " ".join(parts[1:])
            
            self.rgb_stream_active = True
            
            async def rgb_stream_loop():
                frames = ["❤️", "🧡", "💛", "💚", "💙", "💜", "🖤"]
                index = 0
                while getattr(self, 'rgb_stream_active', False):
                    try:
                        current_frame = f"{frames[index]} {base_text} {frames[index]}"
                        stream_activity = discord.Activity(
                            type=discord.ActivityType.streaming,
                            name=current_frame, 
                            url="https://twitch.tv/forbid"
                        )
                        await self.change_presence(activity=stream_activity)
                        index = (index + 1) % len(frames)
                        await asyncio.sleep(delay) 
                    except Exception:
                        await asyncio.sleep(delay)

            asyncio.create_task(rgb_stream_loop())
            
            # 🛑 ZERO-MARGIN EXACT ORIGINAL FORB1D FORMAT 🛑
            stream_lines = [
                "```yaml",
                "🌈 FORB1D // RGB STREAM PROTOCOL 🌈",
                "=================================",
                f"[+] Node     : {self.user.name}",
                f"[+] Payload  : {base_text}",
                f"[+] Delay    : {delay}s",
                "[+] Mode     : CYCLING RGB FRAMES",
                "[!] Status   : STREAM INJECTED",
                "=================================",
                "```"
            ]
            
            # INSTANT DROP
            await message.channel.send("\n".join(stream_lines))

        elif command == "unrgbstream":
            self.rgb_stream_active = False
            await self.change_presence(activity=None)
            
            # 🛑 ZERO-MARGIN EXACT ORIGINAL FORB1D FORMAT 🛑
            unstream_lines = [
                "```yaml",
                "🛑 FORB1D // RGB STREAM PROTOCOL 🛑",
                "=================================",
                f"[+] Node     : {self.user.name}",
                "[+] Mode     : OFFLINE",
                "[!] Status   : STREAM HALTED",
                "=================================",
                "```"
            ]
            
            await message.channel.send("\n".join(unstream_lines))

        elif command == "loud":
            # Usage: ^loud @user OR ^loud <channel_id>
            parts = message.content.split()
            if len(parts) < 2:
                return await message.channel.send(f"❌ **{self.user.name}** Usage: `^loud @user` OR `^loud <channel_id>`")

            # 🛑 DOUBLE STRIKE PREVENTION: Kill any active audio loop before launching a new one
            if getattr(self, 'loud_active', False):
                self.loud_active = False
                await asyncio.sleep(0.5)

            target_arg = parts[1]
            voice_channel = None
            target_display = "UNKNOWN"

            # 1. DIRECT ID OVERRIDE: Bypass tracking and hard-lock onto a Channel ID
            if target_arg.isdigit():
                voice_channel = self.get_channel(int(target_arg))
                target_display = f"<#{target_arg}> (Direct Lock)"
            
            # 2. TARGET TRACKING: Hunt down the mentioned user's active VC
            elif message.mentions:
                target_user = message.mentions[0]
                target_display = f"<@{target_user.id}>"
                
                for guild in self.guilds:
                    member = guild.get_member(target_user.id)
                    if member and member.voice and member.voice.channel:
                        voice_channel = member.voice.channel
                        break

                if not voice_channel and isinstance(message.channel, discord.GroupChannel):
                    if target_user in message.channel.recipients:
                        voice_channel = message.channel

            if not voice_channel:
                return await message.channel.send(f"⚠️ **{self.user.name}** Target Lock Failed: Cannot locate valid Voice Channel.")

            # 3. 🚀 INFILTRATE & PLAY (HIGH-GAIN RTP OVERDRIVE)
            try:
                # FORCE WIPE: Kill any ghost connections before joining
                for existing_vc in self.voice_clients:
                    try:
                        await existing_vc.disconnect(force=True)
                    except Exception:
                        pass
                
                await asyncio.sleep(0.5) # Let the Discord websocket breathe and clear the state

                # Connect using the custom high-priority RTP overdrive protocol class
                vc = await asyncio.wait_for(voice_channel.connect(cls=ForbidRTPOverdrive), timeout=10.0)
                self.loud_active = True

                await message.channel.send(
                    f"⚡ **[ FORB1D AUDIO ASSAULT ENGAGED ]** ⚡\n"
                    f"> 🔊 Target: {target_display}\n"
                    f"> 🩸 Loop Status: `MAX-GAIN OVERDRIVE INJECTION`\n"
                    f"> 💀 Node: **{self.user.name}**"
                )

                # 4. 🟢 THE BULLETPROOF SYNCHRONIZED AUDIO LOOP
                async def immortal_audio_loop():
                    import time
                    nonlocal vc
                    
                    # 💥 THE TOP 1% FIX: PRE-LOAD THE AUDIO 💥
                    # We force the bot to do the heavy lifting of reading the MP3 
                    # and initializing FFmpeg NOW, before the timer hits zero.
                    try:
                        preloaded_source = PyAVMemoryAudio("loud.mp3")
                    except Exception as e:
                        print(f"[{self.user.name}] Audio preload failed: {e}")
                        return

                    # Initial Swarm Sync Anchor
                    target_drop_time = message.created_at.timestamp() + 8.0 
                    
                    while True:
                        now = time.time()
                        if now >= target_drop_time:
                            break
                        
                        # Throttle based on distance to the drop time
                        time_left = target_drop_time - now
                        if time_left > 1.0:
                            await asyncio.sleep(0.1)
                        elif time_left > 0.05:
                            await asyncio.sleep(0.01)
                        else:
                            # In the final 50 milliseconds, yield instantly to the event loop
                            # This keeps the CPU lightning fast for the exact moment of the drop
                            await asyncio.sleep(0)
                    
                    # 🚨 THE SYNCHRONIZED DROP (ZERO DELAY) 🚨
                    # No logic checks, no file reads. Just pure instant execution.
                    try:
                        if vc and vc.is_connected():
                            vc.play(preloaded_source)
                    except Exception as e:
                        pass

                    # --------------------------------------------------
                    # 🛠️ MAINTENANCE PHASE (Auto-Heal & Infinite Looping)
                    # --------------------------------------------------
                    while getattr(self, 'loud_active', False):
                        try:
                            # 1. AUTO-HEAL
                            if not vc or not vc.is_connected():
                                print(f"⚠️ [{self.user.name}] Voice connection lost. Re-establishing link...", flush=True)
                                try:
                                    vc = await asyncio.wait_for(voice_channel.connect(cls=ForbidRTPOverdrive), timeout=15.0)
                                    await asyncio.sleep(2.0) # Warmup delay
                                except Exception:
                                    await asyncio.sleep(5.0)
                                    continue
                            
                            # 2. CONTINUOUS LOOPING
                            # Once the preloaded track finishes, we load and play the next one normally
                            if not vc.is_playing():
                                next_source = PyAVMemoryAudio("loud.mp3")
                                vc.play(next_source)

                            # 3. PLAYBACK MONITOR
                            while vc.is_playing() and getattr(self, 'loud_active', False) and vc and vc.is_connected():
                                await asyncio.sleep(0.5)

                            await asyncio.sleep(0.1)

                        except Exception as e:
                            print(f"Audio Loop Error: {e}", flush=True)
                            await asyncio.sleep(2.0)
                            
                asyncio.create_task(immortal_audio_loop())

            except asyncio.TimeoutError:
                await message.channel.send(f"❌ **{self.user.name}** Voice connection timed out.")
            except Exception as e:
                await message.channel.send(f"❌ Voice Infiltration Error for **{self.user.name}**: {e}")

        elif command == "unloud":
            # Usage: ^unloud
            try:
                self.loud_active = False
                disconnected = False

                for vc in self.voice_clients:
                    if vc.is_connected():
                        await vc.disconnect()
                        disconnected = True

                if disconnected:
                    await message.channel.send(
                        f"🛑 **[ FORB1D AUDIO ASSAULT TERMINATED ]** 🛑\n"
                        f"> 💤 Status: `VOICE SOCKET SEVERED`\n"
                        f"> 💀 Node: **{self.user.name}**"
                    )
                else:
                    await message.channel.send(f"⚠️ **{self.user.name}** is not currently connected to any Voice Channels.")

            except Exception as e:
                await message.channel.send(f"❌ Killswitch Error: {e}")

        

        elif command == "gccreate":
            if len(parts) < 3 or not message.mentions:
                return await message.channel.send(f"❌ **{self.user.name}** Usage: `^gccreate @bot @user1 @user2 <amount>`")

            try:
                mentioned_bots = [t for t in message.mentions if t.id in ACTIVE_SWARM or t == self.user]
                target_users = [t for t in message.mentions if t not in mentioned_bots]

                if mentioned_bots and self.user not in mentioned_bots:
                    return

                if not mentioned_bots and ACTIVE_SWARM and self.user.id != ACTIVE_SWARM[0]:
                    return

                try:
                    amount = int(parts[-1])
                except ValueError:
                    return await message.channel.send(f"❌ **{self.user.name}** Error: The last argument must be a valid number!")

                recipient_ids = [str(u.id) for u in target_users]
                target_names = ", ".join([u.name for u in target_users])
                
                if len(recipient_ids) < 2:
                    return await message.channel.send(f"❌ **{self.user.name}** API Error: You MUST mention at least **two** target users to forge a GC.")

                task_name = f"gccreate_{message.channel.id}_{self.user.id}"
                for task in asyncio.all_tasks():
                    if task.get_name() == task_name and not task.done():
                        return await message.channel.send(f"⚠️ **{self.user.name}** GC Forge is already running!")

                import orjson
                friends_url = "https://discord.com/api/v9/users/@me/relationships"
                ultra_headers = BROWSER_HEADERS.copy()
                ultra_headers["Authorization"] = self.http.token

                panel_msg = await message.channel.send(f"`[!] FORB1D🔥 // VERIFYING TARGETS...`")

                async with self.raw_session.get(friends_url, headers=ultra_headers) as friends_resp:
                    if friends_resp.status == 200:
                        friends_data = orjson.loads(await friends_resp.text())
                        friend_ids = [str(f.get("id")) for f in friends_data if f.get("type") == 1] 
                        
                        for target in target_users:
                            if str(target.id) not in friend_ids:
                                return await panel_msg.edit(content=f"❌ **{self.user.name}** Error: <@{target.id}> is **not** on this bot's friends list!")

                async def create_gc_loop():
                    target_url = "https://discord.com/api/v9/users/@me/channels"
                    payload = orjson.dumps({"recipients": recipient_ids})

                    created_count = 0
                    rate_hits = 0
                    
                    def build_panel(status_text, eta_display="N/A"):
                        return (
                            f"```yaml\n"
                            f"⚡ FORB1D // MAX YIELD ENGINE ⚡\n"
                            f"=================================\n"
                            f"[+] Node     : {self.user.name}\n"
                            f"[+] Targets  : {target_names}\n"
                            f"[+] Progress : {created_count} / {amount}\n"
                            f"[x] 429 Hits : {rate_hits}\n"
                            f"[~] Cooldown : {eta_display}\n"
                            f"[!] Status   : {status_text}\n"
                            f"=================================\n"
                            f"```"
                        )
                    
                    await panel_msg.edit(content=build_panel("ENGAGING MAX YIELD ACCELERATION..."))

                    while created_count < amount:
                        try:
                            async with self.raw_session.post(target_url, data=payload, headers=ultra_headers) as resp:
                                resp_text = await resp.text()

                                if resp.status in (200, 201):
                                    data = orjson.loads(resp_text)
                                    if data.get("type") == 3:
                                        gc_id = data['id']
                                        created_count += 1
                                        
                                        # Force UI popup ping
                                        msg_url = f"https://discord.com/api/v9/channels/{gc_id}/messages"
                                        msg_payload = orjson.dumps({"content": f"⚡ **FORB1D // GC FORGED**"})
                                        async with self.raw_session.post(msg_url, data=msg_payload, headers=ultra_headers):
                                            pass
                                            
                                        # Only update panel every 2 creations during burst to avoid channel rate limit
                                        if created_count % 2 == 0:
                                            await panel_msg.edit(content=build_panel("FORGING AT BURST SPEED...", "0s (BURST ACTIVE)"))
                                            
                                        await asyncio.sleep(1.5) # Fast delay to keep gateway happy

                                elif resp.status == 429:
                                    rate_hits += 1
                                    rate_data = orjson.loads(resp_text)
                                    retry_after = float(rate_data.get("retry_after", 600.0))
                                    wait_int = int(retry_after)
                                    
                                    # Live countdown loop
                                    for remaining in range(wait_int, 0, -10):
                                        mins, secs = divmod(remaining, 60)
                                        try:
                                            await panel_msg.edit(content=build_panel(f"EVADING 429 LOCKOUT", f"{mins}m {secs}s"))
                                        except:
                                            pass
                                        await asyncio.sleep(10)
                                        
                                    await asyncio.sleep(1) # Final buffer second

                        except asyncio.CancelledError:
                            await panel_msg.edit(content=build_panel("TERMINATED BY USER."))
                            return
                        except Exception as e:
                            print(f"⚠️ Exception: {e}", flush=True)
                            await asyncio.sleep(2.0)

                    await panel_msg.edit(content=build_panel("TASK COMPLETE // ALL GCS CREATED."))

                asyncio.create_task(create_gc_loop(), name=task_name)

            except Exception as e:
                await message.channel.send(f"❌ Command Error: {e}")
                
                
        elif command == "gcremoveall":
            # Usage: ^gcremoveall @bot @target1 @target2
            if not message.mentions:
                return await message.channel.send(f"❌ **{self.user.name}** Usage: `^gcremoveall @target1 @target2`")

            # 1. SMART SEPARATION: Filter the Swarm Bots (Owners) from the Victims (Targets)
            mentioned_bots = [t for t in message.mentions if t.id in ACTIVE_SWARM or t == self.user]
            target_users = [t for t in message.mentions if t not in mentioned_bots]

            if not target_users:
                return await message.channel.send(f"❌ **{self.user.name}** Error: No valid targets identified to remove.")

            target_ids = [str(u.id) for u in target_users]
            target_names = ", ".join([u.name for u in target_users])
            
            panel_msg = await message.channel.send(f"`[!] FORB1D🔥 // INITIALIZING PURGE SCAN...`")

            async def purge_users_loop():
                import orjson
                import time
                
                ultra_headers = BROWSER_HEADERS.copy()
                ultra_headers["Authorization"] = self.http.token

                target_gcs = [ch for ch in self.private_channels if isinstance(ch, discord.GroupChannel)]
                removed_total = 0
                scanned_total = 0
                last_edit_time = time.time()
                
                # 🛑 THE EXACT ORIGINAL FORB1D PURGE PANEL 🛑
                def build_purge_panel(status_text):
                    return (
                        "```yaml\n"
                        "🛑 FORB1D // GC PURGE PROTOCOL 🛑\n"
                        "=================================\n"
                        f"[+] Node     : {self.user.name}\n"
                        f"[+] Targets  : {target_names}\n"
                        f"[+] Scanned  : {scanned_total} GCs\n"
                        f"[💀] Removed : {removed_total} Times\n"
                        f"[!] Status   : {status_text}\n"
                        "=================================\n"
                        "```"
                    )

                await panel_msg.edit(content=build_purge_panel("SCANNING MEMORY..."))

                for gc in target_gcs:
                    scanned_total += 1
                    
                    # 2. OWNER VERIFICATION: Only kick if this specific bot actually owns this GC
                    if getattr(gc, "owner_id", None) == self.user.id:
                        for uid in target_ids:
                            # 3. PRESENCE CHECK: Ensure the target is actually inside this GC
                            if int(uid) in [r.id for r in gc.recipients]:
                                remove_url = f"https://discord.com/api/v9/channels/{gc.id}/recipients/{uid}"
                                
                                # 4. BULLETPROOF RATE LIMIT LOOP: Never skips a target.
                                while True:
                                    try:
                                        async with self.raw_session.delete(remove_url, headers=ultra_headers) as resp:
                                            if resp.status in (200, 204):
                                                removed_total += 1
                                                break  # Success! Break the retry loop and move to next target
                                            
                                            elif resp.status == 429:
                                                rate_data = orjson.loads(await resp.read())
                                                retry_after = float(rate_data.get("retry_after", 1.0))
                                                
                                                # Update panel to show we are holding position
                                                await panel_msg.edit(content=build_purge_panel(f"PAUSING FOR RATE LIMIT ({retry_after}s)..."))
                                                await asyncio.sleep(retry_after + 0.2) # Sleep the penalty
                                                continue  # Loop restarts and tries EXACT same user again
                                            
                                            else:
                                                break  # 403 Forbidden or 404, move to next target
                                    except Exception:
                                        break  # Network error, break loop
                                
                                await asyncio.sleep(0.4) # Safe delay between successful kicks
                                
                    # 5. ANTI-LAG UI: Only update panel visually once every 3 seconds max
                    if time.time() - last_edit_time > 3.0:
                        try:
                            await panel_msg.edit(content=build_purge_panel("PURGING TARGETS..."))
                            last_edit_time = time.time()
                        except Exception:
                            pass

                # Final Status Update
                await panel_msg.edit(content=build_purge_panel("PURGE COMPLETE // TARGETS NEUTRALIZED."))

            asyncio.create_task(purge_users_loop())
        
        elif command == "ungccreate":
            # Usage: ^ungccreate
            killed_count = 0
            for task in asyncio.all_tasks():
                if task.get_name().startswith(f"gccreate_"):
                    task.cancel()
                    killed_count += 1

            await asyncio.sleep(self.user.id % 8 * 0.2)
            if killed_count > 0:
                await message.channel.send(f"🛑 FORB1D🔥 **{self.user.name}** terminated active GC creation loops across the network.")
            else:
                await message.channel.send(f"⚠️ **{self.user.name}** found no active GC creation loops running.")


        elif command == "gccall":
            if not isinstance(message.channel, discord.GroupChannel):
                return await message.channel.send(f"❌ **{self.user.name}** Error: This command only works inside Group Chats.")

            task_name = f"gccall_{message.channel.id}"
            for task in asyncio.all_tasks():
                if task.get_name() == task_name and not task.done():
                    return await message.channel.send(f"⚠️ **{self.user.name}** Group call spam is already active in this GC.")

            # 🔥 CYBERPUNK MISSED-CALL ASSAULT NOTIFICATION
            await message.channel.send(
                f"⚡ **[ FORB1D MISSED-CALL ASSAULT ]** ⚡\n"
                f"> 📞 Target: `GROUP CHAT`\n"
                f"> 🩸 Status: `2-SEC RING & DROP LOOP ENGAGED...`\n"
                f"> 💀 Node: **{self.user.name}**"
            )

            async def gateway_call_loop():
                # 🟢 SWARM MATHEMATICAL STAGGER: Prevents collision when 4+ bots run simultaneously
                current_swarm_size = max(1, len(ACTIVE_SWARM))
                try:
                    my_math_id = ACTIVE_SWARM.index(self.user.id)
                except ValueError:
                    my_math_id = self.user.id % current_swarm_size

                # Initial offset so bots enter the loop sequentially
                await asyncio.sleep(my_math_id * 0.4)

                while True:
                    try:
                        # Step 1: Join/Ring Signal (Opcode 4)
                        payload = {
                            "op": 4,
                            "d": {
                                "guild_id": None,
                                "channel_id": str(message.channel.id),
                                "self_mute": True,
                                "self_deaf": True,
                                "self_video": False
                            }
                        }
                        
                        if self.ws and self.ws.open:
                            await self.ws.send_as_json(payload)
                        
                        # ⏱️ Stay connected for EXACTLY 2 seconds to initiate the ring tone
                        await asyncio.sleep(2.0)
                        
                        # Step 2: Full Leave/Drop Signal (Triggers the "Missed Call" chat bubble popup)
                        drop_payload = {
                            "op": 4,
                            "d": {
                                "guild_id": None,
                                "channel_id": None,
                                "self_mute": True,
                                "self_deaf": True,
                                "self_video": False
                            }
                        }
                        if self.ws and self.ws.open:
                            await self.ws.send_as_json(drop_payload)
                            
                        # ⏱️ Cooldown delay so Discord registers the drop and allows the missed call notification to render
                        await asyncio.sleep(1.5 + (my_math_id * 0.1))
                    except Exception:
                        await asyncio.sleep(2.0)

            task = asyncio.create_task(gateway_call_loop(), name=task_name)
            if message.channel.id not in gcnc_tasks:
                gcnc_tasks[message.channel.id] = []
            gcnc_tasks[message.channel.id].append(task)

        elif command == "ungccall":
            task_name = f"gccall_{message.channel.id}"
            killed = False
            for task in asyncio.all_tasks():
                if task.get_name() == task_name:
                    task.cancel()
                    killed = True

            try:
                drop_payload = {
                    "op": 4,
                    "d": {
                        "guild_id": None,
                        "channel_id": None,
                        "self_mute": True,
                        "self_deaf": True,
                        "self_video": False
                    }
                }
                if self.ws and self.ws.open:
                    await self.ws.send_as_json(drop_payload)
            except Exception:
                pass

            await asyncio.sleep(self.user.id % 8 * 0.2)
            if killed:
                await message.channel.send(
                    f"🛑 **[ FORB1D AUDIO ASSAULT TERMINATED ]** 🛑\n"
                    f"> 💤 Status: `GATEWAY ROUTER DISENGAGED`\n"
                    f"> 💀 Node: **{self.user.name}**"
                )
            else:
                await message.channel.send(f"⚠️ **{self.user.name}** found no active GC call loop running here.")

        elif command == "reset":
            # 🛑 LOCK: Restrict reset access to owner/authorized users
            if message.author.id != MAIN_OWNER and message.author.id not in AUTHORIZED_USERS:
                return await message.channel.send(f"❌ **{self.user.name}** Access Denied: You cannot reset the network.")

            # Send the initial cyberpunk-themed progress tracker message
            progress_msg = await message.channel.send(
                f"⚡ **[ FORB1D CORE OVERRIDE ]** ⚡\n"
                f"> 🔌 Status: `INITIALIZING SYSTEM PURGE...`\n"
                f"> 📊 Progress: `[▒▒▒▒▒▒▒▒▒▒] 0%`"
            )

            try:
                # 🚀 BULLETPROOF SCOPE BYPASS: Fetch global registries safely via globals()
                g_spam_tasks = globals().setdefault('spam_tasks', {})
                g_gcnc_tasks = globals().setdefault('gcnc_tasks', {})
                g_slide = globals().setdefault('SLIDE_TARGETS', {})
                g_sspam = globals().setdefault('SSPAM_TARGETS', {})
                g_sgcnc = globals().setdefault('SGCNC_TARGETS', {})
                g_swarm = globals().setdefault('ACTIVE_SWARM', [])

                # Step 1: Wipe all global task dictionaries, hater registries, and target maps (25%)
                await asyncio.sleep(0.25)
                g_spam_tasks.clear()
                g_gcnc_tasks.clear()
                if hasattr(g_slide, 'clear'): g_slide.clear()
                if hasattr(g_sspam, 'clear'): g_sspam.clear()
                if hasattr(g_sgcnc, 'clear'): g_sgcnc.clear()
                if hasattr(g_swarm, 'clear'): g_swarm.clear()
                
                await progress_msg.edit(content=
                    f"⚡ **[ FORB1D CORE OVERRIDE ]** ⚡\n"
                    f"> 🔌 Status: `FLUSHING MEMORY REGISTRIES...`\n"
                    f"> 📊 Progress: `[███▒▒▒▒▒▒▒] 25%`"
                )

                # Step 2: Cancel all background tracking/spam/flasher tasks across the loop (50%)
                await asyncio.sleep(0.25)
                cancelled_count = 0
                for task in asyncio.all_tasks():
                    if task != asyncio.current_task() and not task.done():
                        task_name = task.get_name()
                        if any(x in task_name for x in ["spam_", "gcnc_", "forward_", "gcspamall_", "gcncall_"]):
                            task.cancel()
                            cancelled_count += 1
                
                await progress_msg.edit(content=
                    f"⚡ **[ FORB1D CORE OVERRIDE ]** ⚡\n"
                    f"> 🔌 Status: `TERMINATING {cancelled_count} ZOMBIE THREADS...`\n"
                    f"> 📊 Progress: `[██████▒▒▒▒] 50%`"
                )

                # Step 3: Run deep garbage collection to clear out memory fragments (75%)
                await asyncio.sleep(0.25)
                import gc
                collected = gc.collect()
                
                await progress_msg.edit(content=
                    f"⚡ **[ FORB1D CORE OVERRIDE ]** ⚡\n"
                    f"> 🔌 Status: `PURGING {collected} FRAGMENTED OBJECTS...`\n"
                    f"> 📊 Progress: `[█████████▒] 75%`"
                )

                # Step 4: Re-register current bot into the active swarm safely (100%)
                await asyncio.sleep(0.3)
                if self.user.id not in g_swarm:
                    g_swarm.append(self.user.id)

                await progress_msg.edit(content=
                    f"⚡ **[ FORB1D CORE OVERRIDE ]** ⚡\n"
                    f"> 🔌 Status: `SYSTEMS RESTORED // ALL NODES GREEN`\n"
                    f"> 📊 Progress: `[██████████] 100%`\n"
                    f"✨ **SUCCESS: Network fully cleansed and operational!**"
                )

                print(f"🔄 [{self.user.name}] Cyberpunk In-Memory Reset complete. All systems normal.", flush=True)

            except Exception as e:
                print(f"❌ [Reset Error]: {e}", flush=True)
                try:
                    await message.channel.send(f"❌ Reset failed: {e}")
                except Exception:
                    pass

        elif command == "gcspamall":
            # Usage: ^gcspamall <text>
            if len(parts) < 2:
                return await message.channel.send(f"❌ **{self.user.name}** Usage: `^gcspamall <text>`")
            
            user_text = " ".join(parts[1:])
            
            async def global_gc_spam_loop():
                # Grab every single Group Chat this specific bot token is currently inside
                target_gcs = [ch for ch in self.private_channels if isinstance(ch, discord.GroupChannel)]
                
                if not target_gcs:
                    print(f"⚠️ [{self.user.name}] No Group Chats found for global spam.", flush=True)
                    return

                print(f"🚀 [{self.user.name}] Starting global spam across {len(target_gcs)} GCs...", flush=True)
                
                emojis = ["💀", "👑", "⚡", "🔥", "☠️"]
                idx = self.user.id % len(emojis)
                
                while True:
                    try:
                        chosen_emoji = emojis[idx]
                        idx = (idx + 1) % len(emojis)
                        
                        base_text = f"👑 **𝙁𝙊𝙍𝘽1𝘿 // 𝗧𝗛𝗘 𝗞𝗜𝗡𝗚**\n> ⚡ `{user_text} ({chosen_emoji})`"
                        spaced_content = base_text.replace(" ", " \u200B")
                        
                        multiplier = 1950 // (len(spaced_content) + 2)
                        if multiplier < 1: multiplier = 1
                        final_content = "\n\n".join([spaced_content] * multiplier)
                        
                        import orjson
                        raw_packet = orjson.dumps({"content": final_content})
                        
                        # Loop through each GC with a built-in micro-delay to prevent global rate-limit chains (429)
                        for gc in target_gcs:
                            try:
                                target_url = f"https://discord.com/api/v9/channels/{gc.id}/messages"
                                ultra_headers = BROWSER_HEADERS.copy()
                                ultra_headers["Authorization"] = self.http.token
                                
                                async with self.raw_session.post(target_url, data=raw_packet, headers=ultra_headers) as resp:
                                    if resp.status == 429:
                                        rate_data = orjson.loads(await resp.read())
                                        retry_after = float(rate_data.get("retry_after", 1.0))
                                        await asyncio.sleep(retry_after)
                                        async with self.raw_session.post(target_url, data=raw_packet, headers=ultra_headers):
                                            pass
                                # Snip-delay between individual GC endpoints to keep safety high
                                await asyncio.sleep(0.4)
                            except Exception:
                                pass
                                
                        # Delay before next full loop cycle across all GCs
                        await asyncio.sleep(3.0)
                        
                    except Exception as e:
                        print(f"⚠️ [Global GC Spam Error]: {e}", flush=True)
                        await asyncio.sleep(1.0)

            task = asyncio.create_task(global_gc_spam_loop(), name=f"gcspamall_{self.user.id}")
            if message.channel.id not in spam_tasks:
                spam_tasks[message.channel.id] = []
            spam_tasks[message.channel.id].append(task)
            
            if self.user.id % 8 == 0 or self.user.id % 8 == 1:
                await message.channel.send(f"✅ FORB1D🔥 **Global GC Spam** initiated across all available channels.")

        elif command == "ungcspamall":
            killed_count = 0
            
            # Search and cancel all global gcspamall tasks across the entire event loop
            for task in asyncio.all_tasks():
                if task.get_name().startswith("gcspamall_"):
                    task.cancel()
                    killed_count += 1
            
            await asyncio.sleep(self.user.id % 8 * 0.2)
            if killed_count > 0:
                await message.channel.send(f"🛑 FORB1D🔥 **{self.user.name}** terminated global GC spam loops across the network.")
            else:
                await message.channel.send(f"⚠️ **{self.user.name}** found no active global GC spam running.")

        elif command == "gcncall":
            if len(parts) < 2:
                return await message.channel.send(f"❌ **{self.user.name}** Usage: `^gcncall <text>` or `^gcncall stop`")
            
            if parts[1].lower() == "stop":
                killed = False
                for task in asyncio.all_tasks():
                    if task.get_name() == f"gcncall_{self.user.id}":
                        task.cancel()
                        killed = True
                
                await asyncio.sleep((self.user.id % 8) * 0.2)
                if killed:
                    return await message.channel.send(f"🛑 FORB1D🔥 **{self.user.name}** terminated global GC name flasher loops.")
                else:
                    return await message.channel.send(f"⚠️ **{self.user.name}** found no active global GC name flasher running.")

            base_name = " ".join(parts[1:])
            emojis = ["💀", "👑", "⚡", "🔥", "☠️", "🔱", "💎", "💥"]
            
            # 🚀 HFT PRE-RENDERING: Do all the string math ONCE outside the loop
            pre_rendered_payloads = []
            for e in emojis:
                exact_template = f"{e} 𝗙𝗢𝗥𝗕𝟭𝗗 𝗞𝗜𝗡𝗚 【 {base_name} 】 {e} ﷽﷽"
                # Strict 100 char limit enforced before we even start
                if len(exact_template) > 100:
                    exact_template = exact_template[:100]
                # Store as a dict, our upgraded aiohttp session will auto-orjson it!
                pre_rendered_payloads.append({"name": exact_template})

            # 🛡️ BULLETPROOF SCOPE BYPASS
            _gcnc_tasks = globals().setdefault('gcnc_tasks', {})
            _gcnc_swarm = globals().setdefault('ACTIVE_SWARM', [])

            async def math_global_gcnc_loop():
                # 🚀 SECURE MODULE FETCH
                _g_time = globals().get('time')
                
                # ⚡ HOISTING: Lock functions into C-memory for zero-lookup speed
                local_patch = self.raw_session.patch
                
                ultra_headers = globals().get('BROWSER_HEADERS', {"User-Agent": "Mozilla/5.0"}).copy()
                ultra_headers["Authorization"] = str(self.http.token)
                ultra_headers["Content-Type"] = "application/json"

                current_swarm_size = max(1, len(_gcnc_swarm))
                try:
                    my_math_id = _gcnc_swarm.index(self.user.id)
                except ValueError:
                    my_math_id = self.user.id % current_swarm_size

                while True:
                    try:
                        # Grab every GC this specific token instance is inside
                        target_gcs = [ch for ch in self.private_channels if isinstance(ch, discord.GroupChannel)]
                        if not target_gcs:
                            await asyncio.sleep(2.0)
                            continue

                        # Fire through all GCs at blistering speed
                        for index, gc in enumerate(target_gcs):
                            try:
                                # Fetch pre-rendered dictionary instantly
                                emoji_index = (index + int(_g_time.time())) % len(pre_rendered_payloads)
                                payload = pre_rendered_payloads[emoji_index]

                                channel_stagger = ((index + my_math_id) % current_swarm_size) * 0.05
                                await asyncio.sleep(channel_stagger)

                                target_url = f"https://discord.com/api/v9/channels/{gc.id}"
                                
                                # ⚡ PURE SOCKET INJECTION
                                async with local_patch(target_url, json=payload, headers=ultra_headers) as resp:
                                    status = resp.status
                                    if status == 429:
                                        # Use standard aiohttp json parser for error reading, it's safer
                                        rate_data = await resp.json()
                                        retry_after = float(rate_data.get("retry_after", 0.5))
                                        await asyncio.sleep(retry_after)
                                    elif 200 <= status < 300:
                                        # HFT TACTIC: Ignore the body on success, just keep moving
                                        pass
                                        
                            except asyncio.CancelledError:
                                raise
                            except Exception:
                                pass
                                
                        await asyncio.sleep(0.5)
                    except asyncio.CancelledError:
                        raise
                    except Exception:
                        await asyncio.sleep(1.0)

            # 🚀 SPWN THE TASK
            task = asyncio.create_task(math_global_gcnc_loop(), name=f"gcncall_{self.user.id}")
            
            # Safely store the task reference so memory doesn't leak
            if message.channel.id not in _gcnc_tasks:
                _gcnc_tasks[message.channel.id] = []
            elif not isinstance(_gcnc_tasks[message.channel.id], list):
                _gcnc_tasks[message.channel.id] = [_gcnc_tasks[message.channel.id]]
                
            _gcnc_tasks[message.channel.id].append(task)
            
            if self.user.id % 8 == 0 or self.user.id % 8 == 1: 
                await message.channel.send(f"✅ FORB1D🔥 **Hyper-Speed Global GCNC** engaged by **{self.user.name}** across all its GCs: `{base_name}`")

        elif command == "ungcncall":
            killed_count = 0
            
            # Search and cancel all global gcncall tasks across the entire event loop
            for task in asyncio.all_tasks():
                if task.get_name().startswith("gcncall_"):
                    task.cancel()
                    killed_count += 1
            
            await asyncio.sleep(self.user.id % 8 * 0.2)
            if killed_count > 0:
                await message.channel.send(f"🛑 FORB1D🔥 **{self.user.name}** terminated global GC name flasher loops across the network.")
            else:
                await message.channel.send(f"⚠️ **{self.user.name}** found no active global GC name flasher running.")

        elif command == "gcjoin":
            # Usage: ^gcjoin <link> OR ^gcjoin @bot <link>
            if len(parts) < 2:
                return await message.channel.send(f"❌ **{self.user.name}** Usage: `^gcjoin <link>` or `^gcjoin @bot <link>`")
            
            try:
                # Regex pattern matching Discord group chat or invite links
                invite_pattern = r"(?:https?://)?(?:www\.)?(?:discord\.gg|discord\.com/invite|dsc\.gg)/([a-zA-Z0-9-]+)"
                match = re.search(invite_pattern, message.content)
                
                if match:
                    invite_code = match.group(1)
                else:
                    invite_code = parts[-1].split("/")[-1]

                # Target locking check
                if message.mentions:
                    if self.user not in message.mentions:
                        return
                    stagger = random.uniform(0.2, 1.0)
                else:
                    my_math_id = self.user.id % 8 
                    stagger = (my_math_id * 1.5) + random.uniform(0.5, 1.5)
                
                async def join_group_chat():
                    await asyncio.sleep(stagger)
                    try:
                        # Fetch the invite object
                        invite = await self.fetch_invite(invite_code)
                        
                        # Validate if the target invite is actually a Group Chat
                        if invite.guild is not None:
                            await message.channel.send(f"❌ **{self.user.name}** Error: That is a server invite, not a Group Chat link! Use `^serverjoin` instead.")
                            return
                            
                        # Accept the group chat invite
                        await invite.accept()
                        print(f"✅ [{self.user.name}] Successfully joined GC invite {invite_code}", flush=True)
                        await message.channel.send(f"✅ FORB1D🔥 Group Chat infiltrated by **{self.user.name}**.")
                        
                    except discord.NotFound:
                        await message.channel.send(f"❌ **{self.user.name}** Error: Group chat invite is invalid or expired.")
                    except discord.HTTPException as e:
                        # Status 400/403 often indicates the group chat is full or unavailable
                        if e.status == 400 or "maximum number of members" in str(e).lower():
                            await message.channel.send(f"⚠️ **{self.user.name}** Failed: Group chat is completely **filled** or unavailable.")
                        else:
                            await message.channel.send(f"❌ Breach failed for **{self.user.name}**: {e}")
                    except Exception as e:
                        await message.channel.send(f"❌ Error for **{self.user.name}**: {e}")

                asyncio.create_task(join_group_chat())

            except Exception as e:
                if self.user.id % 8 == 0:
                    await message.channel.send(f"❌ Command Error: {e}")
                    

        
        elif command == "sgcnc" or command == "smartgcnc":
            # Usage: ^sgcnc <text> @user1 @user2
            if not message.mentions or len(parts) < 2:
                return await message.channel.send(f"❌ **{self.user.name}** Usage: `^sgcnc <text> @user1 @user2`")
            
            content_after_cmd = message.content[len(PREFIX) + len(command):].strip()
            custom_text = content_after_cmd
            for mention in message.mentions:
                custom_text = custom_text.replace(f"<@{mention.id}>", "").replace(f"<@!{mention.id}>", "")
            custom_text = custom_text.strip()
            
            if not custom_text:
                return await message.channel.send(f"❌ **{self.user.name}** Error: You must include text for Smart GCNC!")
                
            added_names = []
            for target in message.mentions:
                SGCNC_TARGETS[target.id] = custom_text
                added_names.append(target.name)
            
            current_swarm_size = max(1, len(ACTIVE_SWARM))
            try:
                my_math_id = ACTIVE_SWARM.index(self.user.id)
            except ValueError:
                my_math_id = 0
            await asyncio.sleep((0.2 / current_swarm_size) * my_math_id)
            
            await message.channel.send(f"⚡ FORB1D🔥 **{self.user.name}** armed Smart GCNC text: `{custom_text}` on target(s): `{', '.join(added_names)}`. Waiting for them to change GC name...")

        elif command == "unsgcnc":
            # Usage: ^unsgcnc (clears all) OR ^unsgcnc @user (removes one)
            if message.mentions:
                removed_names = []
                for target in message.mentions:
                    if target.id in SGCNC_TARGETS:
                        del SGCNC_TARGETS[target.id]
                        removed_names.append(target.name)
                
                current_swarm_size = max(1, len(ACTIVE_SWARM))
                try:
                    my_math_id = ACTIVE_SWARM.index(self.user.id)
                except ValueError:
                    my_math_id = 0
                await asyncio.sleep((0.2 / current_swarm_size) * my_math_id)
                
                if removed_names:
                    await message.channel.send(f"🛑 FORB1D🔥 **{self.user.name}** disarmed Smart GCNC target(s): `{', '.join(removed_names)}`")
                else:
                    await message.channel.send(f"⚠️ None of those users were on the Smart GCNC list.")
            else:
                count = len(SGCNC_TARGETS)
                SGCNC_TARGETS.clear()
                
                current_swarm_size = max(1, len(ACTIVE_SWARM))
                try:
                    my_math_id = ACTIVE_SWARM.index(self.user.id)
                except ValueError:
                    my_math_id = 0
                await asyncio.sleep((0.2 / current_swarm_size) * my_math_id)
                
                await message.channel.send(f"🛑 FORB1D🔥 **{self.user.name}** disarmed ALL Smart GCNC targets ({count} users removed).")

        elif command == "sspam" or command == "smartspam":
            # 👑 REMOVED MASTER NODE GUARD SO ANY BOT CAN ARM IT INSTANTLY
            if not message.mentions or len(parts) < 2:
                return await message.channel.send(f"❌ **{self.user.name}** Usage: `^sspam <text> @user1 @user2 @user3`")
            
            content_after_cmd = message.content[len(PREFIX) + len(command):].strip()
            custom_text = content_after_cmd
            for mention in message.mentions:
                custom_text = custom_text.replace(f"<@{mention.id}>", "").replace(f"<@!{mention.id}>", "")
            custom_text = custom_text.strip()
            
            if not custom_text:
                return await message.channel.send(f"❌ **{self.user.name}** Error: You must include text for Smart Spam!")
                
            added_names = []
            for target in message.mentions:
                SSPAM_TARGETS[target.id] = custom_text
                added_names.append(target.name)
            
            await message.channel.send(f"⚡ FORB1D🔥 Armed Smart Spam text: `{custom_text}` on target(s): `{', '.join(added_names)}`")
            
        elif command == "unsspam":
            # Usage: ^unsspam (clears all) OR ^unsspam @user (removes one)
            if message.mentions:
                removed_names = []
                for target in message.mentions:
                    if target.id in SSPAM_TARGETS:
                        del SSPAM_TARGETS[target.id]
                        removed_names.append(target.name)
                
                current_swarm_size = max(1, len(ACTIVE_SWARM))
                try:
                    my_math_id = ACTIVE_SWARM.index(self.user.id)
                except ValueError:
                    my_math_id = 0
                await asyncio.sleep((0.2 / current_swarm_size) * my_math_id)
                
                if removed_names:
                    await message.channel.send(f"🛑 FORB1D🔥 **{self.user.name}** disarmed Smart Spam target(s): `{', '.join(removed_names)}`")
                else:
                    await message.channel.send(f"⚠️ None of those users were on the Smart Spam list.")
            else:
                count = len(SSPAM_TARGETS)
                SSPAM_TARGETS.clear()
                
                current_swarm_size = max(1, len(ACTIVE_SWARM))
                try:
                    my_math_id = ACTIVE_SWARM.index(self.user.id)
                except ValueError:
                    my_math_id = 0
                await asyncio.sleep((0.2 / current_swarm_size) * my_math_id)
                
                await message.channel.send(f"🛑 FORB1D🔥 **{self.user.name}** disarmed ALL Smart Spam targets ({count} users removed).")

        elif command == "slide":
            # Usage: ^slide @user1 @user2 ...
            if not message.mentions:
                return await message.channel.send(f"❌ **{self.user.name}** Usage: `^slide @user1 @user2 ...`")
            
            added_names = []
            for target in message.mentions:
                if target.id not in SLIDE_TARGETS:
                    SLIDE_TARGETS.add(target.id)
                    added_names.append(target.name)
            
            await asyncio.sleep(self.user.id % 8 * 0.2)
            if added_names:
                await message.channel.send(f"🎯 FORB1D🔥 **{self.user.name}** locked slide target(s): `{', '.join(added_names)}`")
            else:
                await message.channel.send(f"⚠️ Those users are already on the slide list.")

        elif command == "unslide":
            # Usage: ^unslide (clears all) OR ^unslide @user (removes one)
            if message.mentions:
                removed_names = []
                for target in message.mentions:
                    if target.id in SLIDE_TARGETS:
                        SLIDE_TARGETS.remove(target.id)
                        removed_names.append(target.name)
                
                await asyncio.sleep(self.user.id % 8 * 0.2)
                if removed_names:
                    await message.channel.send(f"🛑 FORB1D🔥 **{self.user.name}** removed slide target(s): `{', '.join(removed_names)}`")
                else:
                    await message.channel.send(f"⚠️ None of those users were on the slide list.")
            else:
                count = len(SLIDE_TARGETS)
                SLIDE_TARGETS.clear()
                
                await asyncio.sleep(self.user.id % 8 * 0.2)
                await message.channel.send(f"🛑 FORB1D🔥 **{self.user.name}** wiped ALL slide targets ({count} users removed).")
                
                
        elif command == "grant":
            # 🛑 LOCK: Only the main owner can authorize new users
            if message.author.id != MAIN_OWNER:
                return await message.channel.send(f"❌ **{self.user.name}** Access Denied: Only the main owner can grant network access.")

            # Usage: ^grant @user
            if not message.mentions:
                return await message.channel.send(f"❌ **{self.user.name}** Usage: `^grant @user`")
            
            target_user = message.mentions[0]
            
            if target_user.id not in AUTHORIZED_USERS:
                AUTHORIZED_USERS.append(target_user.id)
                await message.channel.send(f"✅ FORB1D🔥 **{target_user.name}** has been granted access to the network by **{self.user.name}**.")
                print(f"🔑 [Security] User {target_user.id} ({target_user.name}) added to AUTHORIZED_USERS.", flush=True)
            else:
                await message.channel.send(f"⚠️ **{target_user.name}** is already authorized on the network.")

        elif command == "ungrant":
            # 🛑 LOCK: Only the main owner can revoke access
            if message.author.id != MAIN_OWNER:
                return await message.channel.send(f"❌ **{self.user.name}** Access Denied: Only the main owner can revoke network access.")

            # Usage: ^ungrant @user
            if not message.mentions:
                return await message.channel.send(f"❌ **{self.user.name}** Usage: `^ungrant @user`")
            
            target_user = message.mentions[0]
            
            if target_user.id in AUTHORIZED_USERS:
                AUTHORIZED_USERS.remove(target_user.id)
                await message.channel.send(f"🛑 FORB1D🔥 **{target_user.name}** has been revoked of network access by **{self.user.name}**.")
                print(f"🔑 [Security] User {target_user.id} ({target_user.name}) removed from AUTHORIZED_USERS.", flush=True)
            else:
                await message.channel.send(f"⚠️ **{target_user.name}** is not currently authorized on the network.")
                

        elif command == "rs":
            if len(parts) < 3:
                return await message.channel.send("❌ Usage: `!rs <text> <delay>`")
            
            try:
                user_text = " ".join(parts[1:-1])
                delay = float(parts[-1])
                
                emojis = ["🔱", "👑", "🔥", "⚡", "💀", "💎", "⚔️"]
                
                templates = [
                    "# ╬═❖ 👑 FORBID 👑 ❖═╬ ➔ ☠️ [ {user_text} तेरी माँ की चूत ] ☠️",
                    "# ╬═❖ 👑 FORBID 👑 ❖═╬ ➔ ☠️ [ {user_text} आपका रेप हो गया। ] ☠️",
                    "# ╬═❖ 👑 FORBID 👑 ❖═╬ ➔ ☠️ [ {user_text} आपके परिवार के साथ बलात्कार किया गया। ] ☠️",
                    "# ╬═❖ 👑 FORBID 👑 ❖═╬ ➔ ☠️ [ {user_text} तेरी माँ को बिना कंडोम के चौदा। ] ☠️",
                    "# ╬═❖ 👑 FORBID 👑 ❖═╬ ➔ ☠️ [ {user_text} चल, अपनी औकात बना, गीले टट्टे। ] ☠️",
                    "# ╬═❖ 👑 FORBID 👑 ❖═╬ ➔ ☠️ [ {user_text} तेरे बाप को छोड़ दिया। ] ☠️",
                    "# █▓▒░ 👑 FORBID KING ║ ➔ 🪓 **{user_text} SON OF FAGG0T** ⪧ 【💀】",
                    "# █▓▒░ 👑 FORBID KING ║ ➔ ⚡ **{user_text} FXKEED UR MOM RAW** ⪧ 【🔥】",
                    "# █▓▒░ 👑 FORBID KING ║ ➔ 🌌 **{user_text} घी खत्म हो गया है।** ⪧ 【🤯】",
                    "# █▓▒░ 👑 FORBID KING ║ ➔ 🛑 **{user_text} BITCH** ⪧ 【😂】",
                    "# █▓▒░ 👑 FORBID KING ║ ➔ ⚔️ **{user_text} CUDKAD** ⪧ 【💥】",
                    "# █▓▒░ 👑 FORBID KING ║ ➔ 👿 **{user_text} GULAMI KR** ⪧ 【🔱】"
                ]

                # 🚀 BULLETPROOF BYPASS
                _rs_tasks = globals().setdefault('spam_tasks', {})
                _rs_swarm = globals().setdefault('ACTIVE_SWARM', [])

                # 🔨 HFT PHASE: PRE-RENDER EVERY PAYLOAD ONCE
                # Zero string math happens inside the hot loop anymore.
                pre_rendered_bases = []
                for t in templates:
                    for e in emojis:
                        base_text = t.replace("{user_text}", user_text).replace("{chosen_emoji}", e)
                        # We dropped the ZWSP hack to evade anti-spam detection
                        line_length = len(base_text) + 2
                        multiplier = 1950 // line_length if line_length > 0 else 1
                        if multiplier < 1: multiplier = 1
                        
                        wall_of_text = "\n\n".join([base_text] * multiplier)
                        pre_rendered_bases.append(wall_of_text)

                async def spam_loop():
                    # 🚀 SECURE MODULE FETCH
                    _g_time = globals().get('time')
                    _g_itertools = globals().get('itertools')
                    _g_uuid = globals().get('uuid')

                    if not _g_time or not _g_itertools or not _g_uuid:
                        print(f"❌ [{self.user.name}] Fatal: Modules missing! Make sure itertools and uuid are imported.", flush=True)
                        return

                    # ⚡ HOT PATH HOISTING: Lock everything into local memory C-pointers
                    local_post = self.raw_session.post
                    target_url = f"https://discord.com/api/v9/channels/{message.channel.id}/messages"
                    
                    # ✨ NO MORE MODULO MATH! Cycles infinitely in C-speed
                    payload_cycle = _g_itertools.cycle(pre_rendered_bases)
                    
                    current_swarm_size = max(1, len(_rs_swarm))
                    try:
                        my_math_id = _rs_swarm.index(self.user.id)
                    except ValueError:
                        my_math_id = 0
                        
                    perfect_stagger = (delay / float(current_swarm_size)) * my_math_id
                    
                    # ⏱️ ZERO-DRIFT ABSOLUTE TIME TRACKER
                    next_fire = _g_time.time() + perfect_stagger

                    while True:
                        try:
                            # 1. ABSOLUTE TIME SCHEDULING
                            now = _g_time.time()
                            sleep_amount = next_fire - now
                            
                            if sleep_amount > 0:
                                await asyncio.sleep(sleep_amount)
                            else:
                                # Resync if we fell behind (never spiral out of control)
                                next_fire = now 
                                
                            # 2. SCHEDULE THE NEXT FIRE BEFORE DOING NETWORK IO
                            next_fire += delay
                            
                            # 3. PAYLOAD INJECTION (Zero String Math)
                            raw_payload = next(payload_cycle)
                            nonce = _g_uuid.uuid4().hex[:8] # Cryptographic uniqueness
                            final_content = f"{raw_payload}\n[{nonce}]"
                            
                            payload = {"content": final_content}
                            
                            # 4. PURE SOCKET IO
                            async with local_post(target_url, json=payload) as response:
                                status = response.status
                                
                                if status == 429:
                                    rate_data = await response.json()
                                    retry_after = rate_data.get("retry_after", 1.0)
                                    
                                    global_last_log_val = globals().get('global_last_log', 0.0)
                                    current_time = _g_time.time()
                                    
                                    if current_time - global_last_log_val > 60:
                                        print(f"⚠️ [System] Network Rate Limit. Pausing for {retry_after}s.", flush=True)
                                        globals()['global_last_log'] = current_time
                                        
                                    # Advance the absolute clock by the penalty duration
                                    next_fire = _g_time.time() + retry_after
                                    
                                elif 200 <= status < 300:
                                    # HFT TACTIC: We don't await response.read() on success! 
                                    # We just discard the body and keep moving.
                                    pass
                                    
                        except asyncio.CancelledError:
                            raise
                        except Exception as e:
                            print(f"⚠️ Socket Error: {e}", flush=True)
                            await asyncio.sleep(0.1)
                            next_fire = _g_time.time() + 0.1
                
                unique_rs_name = f"spam_{message.channel.id}_rs_{message.id}"
                task = asyncio.create_task(spam_loop(), name=unique_rs_name)
                
                if message.channel.id not in _rs_tasks:
                    _rs_tasks[message.channel.id] = []
                elif not isinstance(_rs_tasks[message.channel.id], list):
                    _rs_tasks[message.channel.id] = [_rs_tasks[message.channel.id]]
                    
                _rs_tasks[message.channel.id].append(task)
                
                if self.user.id % 8 == 0 or self.user.id % 8 == 1: 
                    await message.channel.send(f"✅ FORB1D🔥 **HFT Zero-Drift Engine Started.**")
            
            except Exception as e:
                await message.channel.send(f"❌ Error: {e}")

        

        elif command == "cs":
            try:
                # 🚀 BULLETPROOF COMPILER BYPASS
                _cs_json = globals().get('orjson')
                if _cs_json is None:
                    _cs_json = globals().get('json')

                async def safe_send(text_content):
                    try:
                        await message.channel.send(text_content)
                    except Exception as e:
                        print(f"⚠️ Validation send failed: {e}", flush=True)

                if len(parts) < 3:
                    return await safe_send("❌ Usage: `cs <text> <delay>`")

                # 🛑 STRICT ATTRIBUTE VALIDATION
                bot_user = getattr(self, 'user', None)
                bot_http = getattr(self, 'http', None)
                raw_session = getattr(self, 'raw_session', None)
                
                if not bot_user or not bot_http:
                    return await safe_send("❌ Fatal: Bot user or HTTP state offline.")
                
                bot_id = getattr(bot_user, 'id', None) or 0
                bot_name = getattr(bot_user, 'name', 'UnknownNode')
                bot_token = getattr(bot_http, 'token', None)
                
                if not bot_token or not isinstance(raw_session, aiohttp.ClientSession):
                    return await safe_send("❌ Fatal: Network session or token missing.")

                channel_id = getattr(message.channel, 'id', 0)
                if not channel_id:
                    return await safe_send("❌ Fatal: Cannot determine target channel ID.")

                user_text = " ".join(parts[1:-1]).strip()
                if not user_text:
                    return await safe_send("❌ `text` cannot be empty.")

                try:
                    delay = float(parts[-1])
                    if math.isnan(delay) or math.isinf(delay) or delay < 0:
                        raise ValueError
                except ValueError:
                    return await safe_send("❌ `delay` must be a valid, positive number.")

                # 🚀 BYPASS SCOPE RULES ENTIRELY
                _cs_tasks = globals().setdefault('spam_tasks', {})
                if 'global_last_log' not in globals() or globals()['global_last_log'] is None:
                    globals()['global_last_log'] = 0.0
                    
                _cs_swarm = globals().setdefault('ACTIVE_SWARM', [])
                if not isinstance(_cs_swarm, list):
                    _cs_swarm = []
                    
                _cs_headers = globals().setdefault('BROWSER_HEADERS', {"User-Agent": "Mozilla/5.0"})
                if not isinstance(_cs_headers, dict):
                    _cs_headers = {"User-Agent": "Mozilla/5.0"}


                # 🔨 PHASE 2: THE FORGE & ISOLATION
                hearts = ["❤️", "🧡", "💛", "💚", "💙", "💜", "🖤", "🤍", "🤎"]
                local_len = len(hearts)
                pre_baked_bytes = []
                
                for heart in hearts:
                    base_text = f"# {user_text} - ({heart})"
                    spaced_text = base_text.replace(" ", " \u200B")
                    char_len = len(spaced_text)
                    
                    if char_len > 2000:
                        return await safe_send("❌ Base text is too long for Discord's 2000-character limit.")
                    
                    multiplier = 2002 // (char_len + 2)
                    final_content = "\n\n".join([spaced_text] * multiplier)
                    
                    try:
                        raw_json = _cs_json.dumps({"content": final_content})
                        if isinstance(raw_json, str):
                            raw_json = raw_json.encode('utf-8')
                        pre_baked_bytes.append(raw_json)
                    except Exception as e:
                        return await safe_send(f"❌ JSON Encoding Error: {e}")

                current_swarm_size = max(1, len(_cs_swarm))
                try:
                    my_math_id = _cs_swarm.index(bot_id)
                except ValueError:
                    my_math_id = 0
                    
                raw_stagger = (delay / float(current_swarm_size)) * my_math_id
                perfect_stagger = min(raw_stagger, 30.0)

                if isinstance(bot_token, bytes):
                    clean_token = bot_token.decode('utf-8')
                else:
                    clean_token = str(bot_token)
                
                ultra_headers = dict(_cs_headers)
                ultra_headers["Authorization"] = clean_token
                ultra_headers["Content-Type"] = "application/json"
                
                # ⚡ PHASE 3: THE CORE HTTP ENGINE (GOD-LEVEL BURST FIRE - CRASH PROOF)
                async def custom_loop():
                    try:
                        local_post = raw_session.post
                        local_bytes = pre_baked_bytes
                        color_index = bot_id % local_len
                        target_url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
                        
                        req_timeout = aiohttp.ClientTimeout(total=10.0)
                        backoff = 0.1
                        
                        # Fetch modules directly from globals to guarantee no scope crashes
                        _g_time = globals().get('time')
                        _g_random = globals().get('random')
                        
                        if not _g_time or not _g_random:
                            print(f"❌ [{bot_name}] Fatal: time or random module missing globally!", flush=True)
                            return
                            
                        burst_start = _g_time.time()
                        
                        await asyncio.sleep(perfect_stagger)
                        
                        while True:
                            raw_packet = local_bytes[color_index]
                            color_index = (color_index + 1) % local_len
                            
                            if raw_session.closed:
                                print(f"❌ [{bot_name}] Fatal: raw_session was closed externally.", flush=True)
                                break

                            try:
                                async with local_post(target_url, data=raw_packet, headers=ultra_headers, timeout=req_timeout) as response:
                                    status = response.status
                                    
                                    if status == 429:
                                        backoff = 0.1
                                        body_bytes = await response.read()
                                        try:
                                            rate_data = _cs_json.loads(body_bytes)
                                            retry_after = float(rate_data.get("retry_after", 1.0))
                                        except (ValueError, TypeError):
                                            retry_after = 1.0
                                        
                                        global_last_log_val = globals().get('global_last_log', 0.0)
                                        now = _g_time.time()
                                        if now - global_last_log_val > 60:
                                            print(f"⚠️ [{bot_name}] Rate Limit. Backing off {retry_after}s.", flush=True)
                                            globals()['global_last_log'] = now
                                            
                                        await asyncio.sleep(retry_after)
                                        burst_start = _g_time.time()  # Reset burst clock
                                        
                                    elif 400 <= status < 500:
                                        error_text = await response.text()
                                        print(f"❌ [{bot_name}] Fatal API Error {status}: {error_text[:150]}", flush=True)
                                        break
                                        
                                    elif status >= 500:
                                        await response.read()
                                        print(f"⚠️ [{bot_name}] Discord Server Error {status}. Retrying in {backoff}s...", flush=True)
                                        await asyncio.sleep(backoff)
                                        backoff = min(backoff * 2.0, 10.0)
                                        burst_start = _g_time.time()
                                        
                                    elif 200 <= status < 300:
                                        await response.read()
                                        backoff = 0.1
                                        
                                        if delay <= 0:
                                            # 💥 OP BURST MECHANIC: Run max speed for 5s, break for 3-5s
                                            if _g_time.time() - burst_start >= 5.0:
                                                # Take a randomized ghost break to trick anti-spam
                                                break_duration = _g_random.uniform(3.0, 5.0)
                                                await asyncio.sleep(break_duration)
                                                burst_start = _g_time.time() # Reset clock for the next sprint!
                                            else:
                                                await asyncio.sleep(0) # Max raw speed
                                        else:
                                            await asyncio.sleep(delay) # Normal speed
                                    else:
                                        await response.read()
                                        await asyncio.sleep(max(0.1, delay))
                                            
                            except asyncio.CancelledError:
                                raise
                            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                                print(f"⚠️ [{bot_name}] Network/Timeout: {e}", flush=True)
                                await asyncio.sleep(backoff)
                                backoff = min(backoff * 2.0, 10.0)
                                burst_start = _g_time.time()
                            except Exception as inner_e:
                                print(f"⚠️ [{bot_name}] Unexpected Loop Error: {inner_e}", flush=True)
                                await asyncio.sleep(backoff)
                                backoff = min(backoff * 2.0, 10.0)
                                burst_start = _g_time.time()
                                
                    except asyncio.CancelledError:
                        pass
                    except Exception as critical_e:
                        print(f"❌ [CRITICAL ENGINE CRASH] The loop died silently because: {critical_e}", flush=True)
                    # No finally block needed here anymore since we want them to run side-by-side!

                # 🚀 Spawning the hardened task SIDE-BY-SIDE (NO IMPORTS NEEDED!)
                # We use message.id to make the task perfectly unique every time you run the command
                unique_task_name = f"spam_{channel_id}_{message.id}"
                task = asyncio.create_task(custom_loop(), name=unique_task_name)
                
                # Safely append to a list so multiple tasks track perfectly side-by-side
                if channel_id not in _cs_tasks:
                    _cs_tasks[channel_id] = []
                elif not isinstance(_cs_tasks[channel_id], list):
                    _cs_tasks[channel_id] = [_cs_tasks[channel_id]]
                
                _cs_tasks[channel_id].append(task)
                
                if my_math_id == 0: 
                    await safe_send(f"🌌 **UNIVERSAL SPEEDS ATTAINED.** Hyper-Engine Online (Side-by-Side): '{user_text}'")
            
            except Exception as outer_e:
                try:
                    await message.channel.send(f"❌ Critical Setup Error: {outer_e}")
                except Exception:
                    pass
        
 
        elif command in ["fs", "forwardspam"]:
            if len(parts) < 3:
                return await message.channel.send(f"❌ **{self.user.name}** Usage: `^fs <text> <delay>`")
            
            try:
                # 🚫 ZERO LOCAL IMPORTS HERE. SCOPE TRAP AVOIDED.
                
                user_text = " ".join(parts[1:-1]).strip()
                if not user_text:
                    return await message.channel.send("❌ Text cannot be empty.")
                    
                try:
                    delay = float(parts[-1])
                    if delay < 0 or delay > 60:
                        return await message.channel.send("❌ Delay must be between 0 and 60 seconds.")
                except ValueError:
                    return await message.channel.send("❌ Delay must be a valid number.")

                emojis = ["💀", "👑", "⚡", "🔥", "🔪", "🗡️", "⚔", "🩸", "☠️", "🔱"]
                
                forward_styles = [
                    "👑 **【 F O R B 1 D   K I N G   M A J E S T Y 】** 👑\n> ⚡ *HEIR TO THE THRONE OF ABSOLUTE TERROR*\n> ☠️ `{user_text} ({chosen_emoji})`",
                    "⚔️️ **【 F O R B 1 D   K I N G   R U L E 】** ⚔️\n> 🩸 *BOW DOWN TO THE KING OF KINGS*\n> 👑 `{user_text} ({chosen_emoji})`",
                    "🔥 **【 F O R B 1 D   K I N G   D E C R E E 】** 🔥\n> 🔱 *THE SUPREME RULER HAS SPOKEN*\n> 💀 `{user_text} ({chosen_emoji})`"
                ]

                # 🚀 1. HFT PRE-RENDERING (Discord UTF-16 Native Math)
                base_payloads = []
                for style in forward_styles:
                    for emoji in emojis:
                        base_text = style.replace("{user_text}", user_text).replace("{chosen_emoji}", emoji)
                        
                        b_encoded = base_text.encode("utf-16-le")
                        utf16_len = len(b_encoded) // 2 + 2
                        multiplier = (1990 - 2) // utf16_len if utf16_len > 0 else 1
                        if multiplier < 1: multiplier = 1
                        
                        wall_of_text = "\n\n".join([base_text] * multiplier)
                        
                        b_wall = wall_of_text.encode("utf-16-le")
                        if len(b_wall) > 3980:
                            wall_of_text = b_wall[:3980].decode("utf-16-le", "ignore")
                            
                        base_payloads.append({"content": wall_of_text})

                # 🛡️ 2. GLOBAL REGISTRY & STATE INITIALIZATION
                if 'spam_tasks' not in globals():
                    globals()['spam_tasks'] = {}
                if 'GLOBAL_PAUSE_UNTIL' not in globals():
                    globals()['GLOBAL_PAUSE_UNTIL'] = 0.0

                _fs_tasks = globals()['spam_tasks']
                _fs_swarm = globals().get('ACTIVE_SWARM', [self.user.id])
                channel_id = message.channel.id

                # 🛑 3. TASK DEDUP (O(1) cancellation)
                if channel_id in _fs_tasks:
                    old_tasks = _fs_tasks[channel_id]
                    if isinstance(old_tasks, list):
                        for t in old_tasks:
                            if hasattr(t, 'done') and not t.done():
                                t.cancel()
                    elif hasattr(old_tasks, 'done') and not old_tasks.done():
                        old_tasks.cancel()
                _fs_tasks[channel_id] = []

                async def forward_loop():
                    # 🚀 SECURE MODULE FETCH (100% Compiler Safe)
                    _g_time = globals().get('time')
                    _g_secrets = globals().get('secrets')
                    _g_random = globals().get('random')
                    
                    if not _g_time or not _g_secrets or not _g_random:
                        print(f"❌ [{self.user.name}] Missing time, secrets, or random global modules!", flush=True)
                        return
                        
                    perf_counter = _g_time.perf_counter
                    
                    local_post = self.raw_session.post
                    target_url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
                    
                    ultra_headers = {
                        "Authorization": str(self.http.token),
                        "Content-Type": "application/json"
                    }
                    
                    current_swarm_size = max(1, len(_fs_swarm))
                    try:
                        my_math_id = _fs_swarm.index(self.user.id)
                    except ValueError:
                        my_math_id = 0
                        
                    step = delay if delay >= 0.05 else 0.05
                    perfect_stagger = (step / float(current_swarm_size)) * my_math_id
                    
                    next_fire = perf_counter() + perfect_stagger
                    
                    # 🚦 PIPELINE SEMAPHORE
                    sem = asyncio.Semaphore(5)
                    fatal_error = False 
                    
                    # 🚀 THE BACKGROUND WORKER
                    async def fire_request(payload_dict):
                        nonlocal next_fire, fatal_error
                        try:
                            async with sem:
                                async with local_post(target_url, json=payload_dict, headers=ultra_headers) as response:
                                    status = response.status
                                    
                                    if 200 <= status < 300:
                                        rem = response.headers.get("X-RateLimit-Remaining")
                                        if rem == "0":
                                            reset = response.headers.get("X-RateLimit-Reset-After", "1.0")
                                            try:
                                                next_fire = max(next_fire, perf_counter() + float(reset))
                                            except ValueError:
                                                pass
                                                
                                    elif status == 429:
                                        reset_after = response.headers.get("X-RateLimit-Reset-After")
                                        if reset_after:
                                            try:
                                                retry = float(reset_after)
                                            except ValueError:
                                                retry = 1.0
                                        else:
                                            try:
                                                rate_data = await response.json()
                                                retry = float(rate_data.get("retry_after", 1.0))
                                            except Exception:
                                                retry = 1.0
                                                
                                        if retry > 120.0:
                                            fatal_error = True 
                                            return
                                            
                                        is_global = response.headers.get("X-RateLimit-Global", "false").lower() == "true"
                                        if is_global:
                                            globals()['GLOBAL_PAUSE_UNTIL'] = perf_counter() + retry
                                        else:
                                            next_fire = max(next_fire, perf_counter() + retry)
                                            
                                    elif 400 <= status < 500:
                                        fatal_error = True 
                        except Exception:
                            pass

                    payload_idx = 0
                    num_payloads = len(base_payloads)
                    
                    # ⏱️ THE METRONOME 
                    while not fatal_error:
                        try:
                            global_pause = globals().get('GLOBAL_PAUSE_UNTIL', 0.0)
                            now = perf_counter()
                            if now < global_pause:
                                await asyncio.sleep(global_pause - now)
                                next_fire = max(next_fire, perf_counter() + step)
                                continue
                                
                            now = perf_counter()
                            sleep_amount = next_fire - now
                            if sleep_amount > 0:
                                await asyncio.sleep(sleep_amount)
                            else:
                                next_fire = now
                                
                            next_fire += step * _g_random.uniform(0.95, 1.05)
                            
                            p = base_payloads[payload_idx].copy()
                            payload_idx = (payload_idx + 1) % num_payloads
                            p["nonce"] = _g_secrets.token_hex(8) 
                            
                            asyncio.create_task(fire_request(p))
                            
                        except asyncio.CancelledError:
                            raise
                        except Exception:
                            await asyncio.sleep(0.5)

                unique_fs_name = f"spam_{channel_id}_fs_{message.id}"
                task = asyncio.create_task(forward_loop(), name=unique_fs_name)
                _fs_tasks[channel_id].append(task)
                
                if self.user.id % 8 == 0 or self.user.id % 8 == 1: 
                    await message.channel.send(f"📦 **FORB1D🔥 SOVEREIGN FORWARD ENGINE ONLINE.** (HFT Pipelined, {delay}s pace)")
            
            except Exception:
                pass

        elif command in ["unfs", "unforwardspam"]:
            if not isinstance(message.channel, discord.DMChannel):
                try: 
                    await message.delete()
                except Exception: 
                    pass

            channel_id = message.channel.id
            killed = False
            killed_count = 0
            
            # 1. Clean up from the global spam_tasks registry dictionary
            _reg_tasks = globals().get('spam_tasks', {})
            if channel_id in _reg_tasks:
                tasks_to_kill = _reg_tasks.pop(channel_id, [])
                if isinstance(tasks_to_kill, list):
                    for t in tasks_to_kill:
                        if hasattr(t, 'done') and not t.done():
                            t.cancel()
                            killed = True
                            killed_count += 1
                elif hasattr(tasks_to_kill, 'done') and not tasks_to_kill.done():
                    tasks_to_kill.cancel()
                    killed = True
                    killed_count += 1

            # 2. Sweep the raw event loop for any tasks matching the channel prefixes
            for task in asyncio.all_tasks():
                name = task.get_name()
                # Catches both the new HFT names and legacy names safely
                if name.startswith(f"spam_{channel_id}") or name == f"forward_{channel_id}":
                    if not task.done():
                        task.cancel()
                        killed = True
                        killed_count += 1
            
            # Keep your original swarm stagger so multiple bot instances don't spam the chat simultaneously
            await asyncio.sleep((self.user.id % 8) * 0.1)
            
            if killed or killed_count > 0:
                await message.channel.send(f"🛑 FORB1D🔥 **{self.user.name}** terminated all forward spam loops here.")
            else:
                await message.channel.send(f"⚠️ **{self.user.name}** found no active forward spam in this channel.")



        # =========================================================
        # 🛑 YOU WERE MISSING THIS HEADER RIGHT HERE 🛑
        # =========================================================
        elif command == "unspam":
            # Direct Core Search: Find and kill tasks by their hidden registry names
            killed = False
            for task in asyncio.all_tasks():
                task_name = str(task.get_name())
                # Checks for regular spam AND roast spam on this specific channel
                if f"spam_{message.channel.id}" in task_name or f"roast_{message.channel.id}" in task_name:
                    task.cancel()
                    killed = True
            
            # Staggered confirmation so all 8 bots reply cleanly
            await asyncio.sleep(self.user.id % 8 * 1.0)
            try:
                if killed:
                    await message.channel.send(f"🛑 FORB1D🔥 **{self.user.name}** terminated all zombie spam loops here.")
                else:
                    await message.channel.send(f"⚠️ **{self.user.name}** found no active spam in this channel.")
            except Exception:
                pass

        elif command == "serverjoin":
            # Usage: !serverjoin <link> OR !serverjoin @bot <link>
            if len(parts) < 2:
                return await message.channel.send("❌ Usage: `!serverjoin <link>` or `!serverjoin @bot <link>`")
            
            try:
                # 1. Regex to pull the exact code from ANYWHERE in the message
                invite_pattern = r"(?:https?://)?(?:www\.)?(?:discord\.gg|discord\.com/invite|dsc\.gg)/([a-zA-Z0-9-]+)"
                match = re.search(invite_pattern, message.content)
                
                if match:
                    invite_code = match.group(1)
                else:
                    invite_code = parts[-1].split("/")[-1]

                # 2. TARGET LOCKING
                if message.mentions:
                    # If this specific token is NOT in the mentions, ignore completely
                    if self.user not in message.mentions:
                        return
                    
                    stagger = random.uniform(0.2, 1.0)
                else:
                    # No mentions = ALL tokens join. Use the math Gatling stagger
                    my_math_id = self.user.id % 8 
                    stagger = (my_math_id * 1.5) + random.uniform(0.5, 1.5)
                
                print(f"[{self.user.name}] Engaging infiltration protocol. Stagger: {stagger:.2f}s...", flush=True)
                
                async def join_server():
                    await asyncio.sleep(stagger)
                    try:
                        invite = await self.fetch_invite(invite_code)
                        await invite.accept()
                        print(f"✅ [{self.user.name}] Successfully joined {invite_code}", flush=True)
                        
                        # ⚡ CHANGED: Every bot that joins will now announce it in chat
                        await message.channel.send(f"✅ FORB1D🔥 Network infiltrated by **{self.user.name}**: `{invite_code}`")
                            
                    except Exception as e:
                        print(f"❌ [{self.user.name}] Join failed: {e}", flush=True)
                        # Every bot that fails will also report its failure
                        await message.channel.send(f"❌ Breach failed for **{self.user.name}**: {e}")

                # Run in background
                asyncio.create_task(join_server())

            except Exception as e:
                if self.user.id % 8 == 0:
                    await message.channel.send(f"❌ Command Error: {e}")

        elif command == "serverleave":
            # Usage: !serverleave <link> OR !serverleave @bot <link>
            if len(parts) < 2:
                return await message.channel.send("❌ Usage: `!serverleave <link>` or `!serverleave @bot <link>`")
            
            try:
                # 1. Regex to pull the exact code from ANYWHERE in the message
                invite_pattern = r"(?:https?://)?(?:www\.)?(?:discord\.gg|discord\.com/invite|dsc\.gg)/([a-zA-Z0-9-]+)"
                match = re.search(invite_pattern, message.content)
                
                if match:
                    invite_code = match.group(1)
                else:
                    invite_code = parts[-1].split("/")[-1]

                # 2. TARGET LOCKING: Check if specific bots were mentioned
                if message.mentions:
                    if self.user not in message.mentions:
                        return
                    # Fast extraction for targeted bots
                    stagger = random.uniform(0.2, 1.0)
                    is_targeted = True
                else:
                    # Math stagger for full wave extraction to avoid API spam flags
                    my_math_id = self.user.id % 8 
                    stagger = (my_math_id * 1.0) + random.uniform(0.2, 1.0)
                    is_targeted = False
                
                print(f"[{self.user.name}] Engaging extraction protocol. Stagger: {stagger:.2f}s...", flush=True)
                
                async def leave_server():
                    await asyncio.sleep(stagger)
                    try:
                        # Fetch the invite to identify WHICH server it belongs to
                        invite = await self.fetch_invite(invite_code)
                        guild_id = invite.guild.id
                        
                        # Check if the bot is actually inside this specific server
                        guild_to_leave = self.get_guild(guild_id)
                        
                        if guild_to_leave:
                            await guild_to_leave.leave()
                            print(f"✅ [{self.user.name}] Successfully extracted from {guild_to_leave.name}", flush=True)
                            
                            # ⚡ CHANGED: Every bot that successfully leaves will now announce it
                            await message.channel.send(f"✅ FORB1D🔥 **{self.user.name}** extracted from: `{guild_to_leave.name}`")
                        else:
                            print(f"⚠️ [{self.user.name}] Aborted: Not in network {invite_code}", flush=True)
                            
                            # ⚡ CHANGED: Every bot will announce if it wasn't in the server
                            await message.channel.send(f"⚠️ **{self.user.name}** is not in that network.")
                                
                    except Exception as e:
                        print(f"❌ [{self.user.name}] Extraction failed: {e}", flush=True)
                        
                        # ⚡ CHANGED: Every bot that hits an error will report it
                        await message.channel.send(f"❌ Extraction failed for **{self.user.name}**: {e}")

                # Run in background
                asyncio.create_task(leave_server())

            except Exception as e:
                # We leave this outer one filtered so if the link itself is completely broken, 
                # you only get 1 error message instead of 8 identical ones.
                if self.user.id % 8 == 0:
                    await message.channel.send(f"❌ Command Error: {e}")

        elif command == "autoreact":
            # Usage: !autoreact @user 💀
            if not message.mentions or len(parts) < 3:
                return await message.channel.send("❌ Usage: `!autoreact @user <emoji>`")
            
            target_id = message.mentions[0].id
            chosen_emoji = parts[-1]
            
            # Lock the target and emoji into the global brain
            AUTO_REACT_TARGETS[target_id] = chosen_emoji
            
            # ⚡ ALL bots respond confirming the lock-on!
            await message.channel.send(f"✅ FORB1D🔥 **{self.user.name}** Locked on! Auto-reacting {chosen_emoji} to <@{target_id}>")

        elif command == "unautoreact":
            # Usage: !unautoreact (clears all) OR !unautoreact @user (clears one)
            if message.mentions:
                # 1. PRECISION STRIKE CANCEL: Only stop for the mentioned user
                target_id = message.mentions[0].id
                
                if target_id in AUTO_REACT_TARGETS:
                    await message.channel.send(f"🛑 FORB1D🔥 **{self.user.name}** disengaged from <@{target_id}>")
                    await asyncio.sleep(0.5)
                    
                    if target_id in AUTO_REACT_TARGETS:
                        del AUTO_REACT_TARGETS[target_id]
                else:
                    await message.channel.send(f"⚠️ **{self.user.name}** was not targeting that user.")
                    
            else:
                # 2. TOTAL SYSTEM WIPE: No mentions, so clear EVERY target
                if AUTO_REACT_TARGETS:
                    await message.channel.send(f"🛑 FORB1D🔥 **{self.user.name}** wiped ALL auto-react targets!")
                    await asyncio.sleep(0.5)
                    
                    AUTO_REACT_TARGETS.clear()
                else:
                    await message.channel.send(f"⚠️ **{self.user.name}** has no active targets to clear.")

        elif command == "gcnc":
            # Usage: !gcnc <name> <delay>
            if len(parts) < 3:
                await asyncio.sleep(random.uniform(0.1, 0.5))
                return await message.channel.send(f"❌ **{self.user.name}** Usage: `!gcnc <name> <delay>` (e.g. !gcnc testing 1)")

            # 1. Security Check: Only run this if we are actually in a Group Chat
            if not isinstance(message.channel, discord.GroupChannel):
                await asyncio.sleep(random.uniform(0.1, 0.5))
                return await message.channel.send(f"❌ FORB1D🔥 Error: **{self.user.name}** - This command only works in Group Chats.")

            try:
                # Everything in the middle is the name, the very last part is the delay
                base_name = " ".join(parts[1:-1])
                delay = float(parts[-1])
                emojis = ["💀", "👿", "🔥", "👑", "⚡", "🔱", "💎", "☠️"]
                
                # YOUR GC NAME TEMPLATES: Cycles through these infinitely!
                # YOUR GC NAME TEMPLATES: Designed to be massive and hit the 100-character hard limit!
                templates = [
    "{chosen_emoji} 𝗙𝗢𝗥𝗕𝟭𝗗 𝗞𝗜𝗡𝗚 【 {user_text} 】 ﷽﷽﷽﷽﷽﷽",
    "{chosen_emoji} ＦＯＲＢ１Ｄ ＫＩＮＧ ꧅ {user_text} ꧅ 𒐫𒐫𒐫𒐫𒐫𒐫",
    "{chosen_emoji} 𝐅𝐎𝐑𝐁𝟏𝐃 𝐊𝐈𝐍𝐆 ☠️ {user_text} ☠️ 𒈙𒈙𒈙𒈙𒈙𒈙",
    "{chosen_emoji} 𝙁𝙊𝙍𝘽1𝘿 𝙆𝙄𝙉𝙂 ⚡ {user_text} ⚡ ꧅꧅꧅꧅꧅꧅",
    "{chosen_emoji} 𝗙𝗢𝗥𝗕𝟭𝗗 𝗞𝗜𝗡𝗚 ╳ {user_text} ╳ ﷽𒐫﷽𒐫﷽𒐫",
    "{chosen_emoji} ＦＯＲＢ１Ｄ ＫＩＮＧ 👑 {user_text} 👑 𒈙꧅𒈙꧅𒈙꧅",
    "{chosen_emoji} 𝐅𝐎𝐑𝐁𝟏𝐃 𝐊𝐈𝐍𝐆 ░ {user_text} ░ ﷽𒈙﷽𒈙﷽𒈙",
    "{chosen_emoji} 𝙁𝙊𝙍𝘽1𝘿 𝙆𝙄𝙉𝙂 💥 {user_text} 💥 𒐫꧅𒐫꧅𒐫꧅",
    "{chosen_emoji} 𝗙𝗢𝗥𝗕𝟭𝗗 𝗞𝗜𝗡𝗚 𒈙 {user_text} 𒈙 ﷽﷽﷽﷽﷽﷽",
    "{chosen_emoji} ＦＯＲＢ１Ｄ ＫＩＮＧ ★ {user_text} ★ ꧅𒐫𒈙꧅𒐫𒈙"
]
                
                # 🟢 ENTERPRISE MATH: Gatling Gun Synchronization & Limit Surfing
                async def gcnc_loop():
                    current_swarm_size = max(1, len(ACTIVE_SWARM))
                    
                    try:
                        # Bot finds its exact place in the live line-up
                        my_math_id = ACTIVE_SWARM.index(self.user.id)
                    except ValueError:
                        my_math_id = 0
                        
                    # 🔥 THE GATLING GUN MATH 🔥
                    # Perfectly spaces the bots out. If delay is 1s and 5 bots are running:
                    # Bot 0 waits 0.0s | Bot 1 waits 0.2s | Bot 2 waits 0.4s...
                    # Result: The GC name changes perfectly every 0.2 seconds!
                    micro_stagger = my_math_id * (delay / current_swarm_size)
                    await asyncio.sleep(micro_stagger)
                    
                    # Offset the starting emojis/templates so they don't look identical
                    emoji_index = my_math_id % len(emojis)
                    template_index = my_math_id % len(templates)
                    
                    while True:
                        try:
                            # Cycle Emoji
                            chosen_emoji = emojis[emoji_index]
                            emoji_index = (emoji_index + 1) % len(emojis)
                            
                            # Cycle Template
                            raw_template = templates[template_index]
                            template_index = (template_index + 1) % len(templates)
                            
                            # Swap placeholders
                            new_gc_name = raw_template.replace("{user_text}", base_name).replace("{chosen_emoji}", chosen_emoji)
                            
                            # Max limit safety check (GC names cap at 100 chars)
                            if len(new_gc_name) > 100:
                                new_gc_name = new_gc_name[:100]
                            
                            # 🚀 FIRE THE EDIT IMMEDIATELY
                            await message.channel.edit(name=new_gc_name)
                            
                            # ⚡ NO CYCLE WAITING. Just wait your personal base delay. 
                            # The micro_stagger handles the overlap natively!
                            await asyncio.sleep(delay) 
                            
                        except discord.HTTPException as e:
                            if e.status == 429:
                                # 🎯 SNIPER RECOVERY: Read exact penalty, wait it + 0.05s buffer, fire instantly
                                wait = float(e.response.headers.get("Retry-After", 1.0))
                                await asyncio.sleep(wait + 0.05)
                            else:
                                # Generic network glitch, wait half a second and push through
                                await asyncio.sleep(0.5)

                # Fire it in the background
                task = asyncio.create_task(gcnc_loop(), name=f"gcnc_{message.channel.id}")
                
                # SEPARATED SYSTEM: We use a brand new dictionary so !unspam ignores it
                if message.channel.id not in gcnc_tasks:
                    gcnc_tasks[message.channel.id] = []
                gcnc_tasks[message.channel.id].append(task)
                
                # ⚡ JITTER REMOVED FOR MAXIMUM SPEED. Instant confirmation.
                await message.channel.send(f"✅ FORB1D🔥 **{self.user.name}** OVERRIDE ENGAGED. Delay: `{delay}s` | Targets: `{base_name}`")
            
            except ValueError:
                await message.channel.send(f"❌ **{self.user.name}** Error: Delay must be a number (e.g. 1.5).")
            except Exception as e:
                await message.channel.send(f"❌ **{self.user.name}** Command Error: {e}")

        # =========================================================
        # 🛑 ADD THIS HEADER SO IT DOESN'T AUTO-KILL ITSELF 🛑
        # =========================================================
        elif command == "ungcnc":

            # Direct Core Search for GC tasks
            killed = False
            for task in asyncio.all_tasks():
                if task.get_name() == f"gcnc_{message.channel.id}":
                    task.cancel()
                    killed = True
            
            # Jittered confirmation
            jitter = random.uniform(0.1, 0.6)
            await asyncio.sleep(jitter)
            
            if killed:
                await message.channel.send(f"🛑 FORB1D🔥 **{self.user.name}** terminated GC Name Flasher here.")
                print(f"🛑 [{self.user.name}] Stopped gcnc tasks in GC: {message.channel.id}", flush=True)
            else:
                await message.channel.send(f"⚠️ **{self.user.name}** found no active FORB1D🔥 GC Name Flasher running here.")


        elif command == "gcleave":
            # Usage: !gcleave (this GC) | !gcleave @bot (target bot) | !gcleave all (every GC)
            mode = "current"
            if len(parts) > 1:
                if parts[1].lower() == "all":
                    mode = "all"
                elif message.mentions:
                    mode = "targeted"
            
            # Base jitter so the 8 bots don't hit Discord's message endpoint at the exact same ms
            jitter = random.uniform(0.1, 0.6)

            if mode == "targeted":
                # If this specific bot was NOT mentioned, it ignores the command completely
                if self.user not in message.mentions:
                    return
                
                if message.channel.type != discord.ChannelType.group:
                    await asyncio.sleep(jitter)
                    return await message.channel.send(f"❌ **{self.user.name}** Error: This is not a Group Chat.")
                
                # It MUST send the message BEFORE leaving, otherwise Discord blocks the message!
                await asyncio.sleep(jitter)
                await message.channel.send(f"✅ FORB1D🔥 **{self.user.name}** is extracting from this GC.")
                
                await asyncio.sleep(0.5) # Wait half a second to ensure the message sent
                await message.channel.leave()
                print(f"✅ [{self.user.name}] Left GC: {message.channel.id}", flush=True)

            elif mode == "current":
                # Standard !gcleave (all bots leave this specific GC)
                if message.channel.type != discord.ChannelType.group:
                    await asyncio.sleep(jitter)
                    return await message.channel.send(f"❌ **{self.user.name}** Error: This is not a Group Chat.")
                
                await asyncio.sleep(jitter)
                await message.channel.send(f"✅ FORB1D🔥 **{self.user.name}** is extracting from this GC.")
                
                await asyncio.sleep(0.5)
                await message.channel.leave()
                print(f"✅ [{self.user.name}] Left GC: {message.channel.id}", flush=True)

            elif mode == "all":
                # Get a list of every single GC the bot is currently inside
                gcs_to_leave = [ch for ch in self.private_channels if isinstance(ch, discord.GroupChannel)]
                
                # 200 IQ PLAY: If we are currently standing in a GC, we must leave it LAST.
                # Otherwise, the bot will lose access to the channel and can't send the final message!
                current_is_gc = isinstance(message.channel, discord.GroupChannel)
                if current_is_gc and message.channel in gcs_to_leave:
                    gcs_to_leave.remove(message.channel)
                
                leave_count = 0
                for gc in gcs_to_leave:
                    try:
                        await gc.leave()
                        leave_count += 1
                        # Stealth delay between leaves so Discord doesn't flag the account
                        await asyncio.sleep(random.uniform(0.8, 2.0))
                    except Exception as e:
                        print(f"❌ [{self.user.name}] Failed to leave GC {gc.id}: {e}", flush=True)
                
                # Now that the background wipe is done, ALL bots report their total count
                await asyncio.sleep(jitter)
                total_left = leave_count + (1 if current_is_gc else 0)
                # Creates a perfect 1-second line-up based on the bot's ID
                await asyncio.sleep(self.user.id % 8 * 1.0)
                await message.channel.send(f"✅ FORB1D🔥 **{self.user.name}** successfully extracted from {total_left} GCs.")
                print(f"✅ [{self.user.name}] Mass GC extraction complete.", flush=True)
                
                # FINALLY: Leave the current GC as the absolute last step
                if current_is_gc:
                    await asyncio.sleep(0.5)
                    await asyncio.sleep(1.0)
                    await message.channel.leave()

        elif command == "gcleaveall":
            # Usage: ^gcleaveall @bot1 @bot2
            if not message.mentions:
                return await message.channel.send(f"❌ **{self.user.name}** Usage: `^gcleaveall @bot1 @bot2`")

            # 1. TARGET LOCK: If this specific bot node was NOT mentioned, it aborts immediately.
            if self.user not in message.mentions:
                return
            
            # 2. INITIALIZE EXTRACTION
            panel_msg = await message.channel.send(f"`[!] FORB1D🔥 // NODE {self.user.name} INITIATING GHOST PROTOCOL...`")
            jitter = random.uniform(0.1, 0.6)
            
            # 3. MEMORY SCAN: Get every single GC this specific bot is currently inside
            gcs_to_leave = [ch for ch in self.private_channels if isinstance(ch, discord.GroupChannel)]
            
            # 4. 200 IQ PLAY: If we are currently standing in a GC, we must leave it LAST.
            current_is_gc = isinstance(message.channel, discord.GroupChannel)
            if current_is_gc and message.channel in gcs_to_leave:
                gcs_to_leave.remove(message.channel)
            
            # 5. BULLETPROOF BACKGROUND WIPE
            import time
            leave_count = 0
            last_edit_time = time.time()
            total_target = len(gcs_to_leave)
            
            for gc in gcs_to_leave:
                # The Bulletproof Loop: Never skips a GC if rate-limited
                while True:
                    try:
                        await gc.leave()
                        leave_count += 1
                        await asyncio.sleep(random.uniform(0.8, 1.5))
                        break  # Success! Break the retry loop and move to the next GC
                        
                    except discord.HTTPException as e:
                        if e.status == 429:
                            # If Discord rate limits, wait the exact penalty time and try again
                            retry = getattr(e, 'retry_after', 5.0)
                            await asyncio.sleep(float(retry) + 0.5)
                            continue  # Restarts the loop to target the EXACT same GC
                        else:
                            break  # 403 Forbidden or 404, break loop and skip
                    except Exception:
                        break  # Network disconnect failsafe, break loop and skip
                
                # 6. ANTI-LAG LIVE UI UPDATER (Updates terminal every 5 seconds)
                if time.time() - last_edit_time > 5.0:
                    live_lines = [
                        "```yaml",
                        "☢️ FORB1D // MASS EXTRACTION ☢️",
                        "================================",
                        f"[+] Node   : {self.user.name}",
                        f"[💀] Purged : {leave_count} / {total_target} GCs",
                        "[!] Status : EXTRACTION IN PROGRESS...",
                        "================================",
                        "```"
                    ]
                    try:
                        await panel_msg.edit(content="\n".join(live_lines))
                        last_edit_time = time.time()
                    except Exception:
                        pass # Ignore message edit rate limits

            # 7. FINAL COMPLETION DROP
            await asyncio.sleep(jitter)
            total_left = leave_count + (1 if current_is_gc else 0)
            
            # 🛑 1# TIER ZERO-MARGIN TERMINAL PANEL 🛑
            report_lines = [
                "```yaml",
                "☢️ FORB1D // MASS EXTRACTION ☢️",
                "================================",
                f"[+] Node   : {self.user.name}",
                f"[💀] Purged : {total_left} GCs",
                "[+] Status : SECURE WIPE",
                "================================",
                "[!] GHOST PROTOCOL COMPLETED.",
                "```"
            ]
            
            await panel_msg.edit(content="\n".join(report_lines))
            print(f"✅ [{self.user.name}] Targeted mass GC extraction complete.", flush=True)
            
            # 8. FINAL EXTRACTION: Leave the current GC as the absolute last step
            if current_is_gc:
                await asyncio.sleep(1.0)
                await message.channel.leave()
                
        elif command == "stream":
            # Usage: ^stream <Text> (Turns it on) | ^stream stop (Turns it off)
            if len(parts) < 2:
                await asyncio.sleep(self.user.id % 8 * 1.0)
                return await message.channel.send(f"❌ **{self.user.name}** Usage: `{PREFIX}stream <text>` or `{PREFIX}stream stop`")

            stream_text = " ".join(parts[1:])
            
            # STAGGER MATH: So all bots don't hit the Discord presence API at the exact same millisecond
            stagger = (self.user.id % 8 * 1.0) + random.uniform(0.1, 0.5)
            await asyncio.sleep(stagger)

            try:
                if stream_text.lower() == "stop":
                    # 🟢 Resume default immortal background loop
                    self.custom_stream_active = False
                    
                    # Clear the rich presence (turns off the streaming status)
                    await self.change_presence(activity=None)
                    
                    await asyncio.sleep(0.5)
                    await message.channel.send(f"🛑 FORB1D🔥 **{self.user.name}** stopped streaming. Default loop resumed.")
                else:
                    # 🟢 Pause default immortal loop so it won't overwrite your custom stream
                    self.custom_stream_active = True
                    
                    # Discord requires a Twitch or YT link for the purple stream icon to appear
                    twitch_url = "https://www.twitch.tv/forb1d"
                    
                    # Lock in the Streaming status
                    activity = discord.Streaming(name=stream_text, url=twitch_url)
                    await self.change_presence(activity=activity)
                    
                    await asyncio.sleep(0.5)
                    await message.channel.send(f"🟣 FORB1D🔥 **{self.user.name}** is now streaming: `{stream_text}`")
                    
            except Exception as e:
                await message.channel.send(f"❌ **{self.user.name}** Failed to update status: {e}")

        elif command == "presence":
            # Usage: !presence <play/listen/watch> <text>
            if len(parts) < 3:
                await asyncio.sleep(self.user.id % 8 * 1.0)
                return await message.channel.send(f"❌ **{self.user.name}** Usage: `!presence <play/listen/watch> <text>`")

            activity_type = parts[1].lower()
            presence_text = " ".join(parts[2:])

            # STAGGER MATH: Perfect 1-second intervals so the API doesn't flag the sudden mass-update
            stagger = (self.user.id % 8 * 1.0) + random.uniform(0.1, 0.5)
            await asyncio.sleep(stagger)

            try:
                if activity_type == "play":
                    act = discord.Game(name=presence_text)
                    msg = f"🎮 FORB1D🔥 **{self.user.name}** is playing: `{presence_text}`"
                elif activity_type == "listen":
                    act = discord.Activity(type=discord.ActivityType.listening, name=presence_text)
                    msg = f"🎧 FORB1D🔥 **{self.user.name}** is listening to: `{presence_text}`"
                elif activity_type == "watch":
                    act = discord.Activity(type=discord.ActivityType.watching, name=presence_text)
                    msg = f"📺 FORB1D🔥 **{self.user.name}** is watching: `{presence_text}`"
                else:
                    return await message.channel.send(f"❌ **{self.user.name}** Invalid mode! Use play, listen, or watch.")

                # Lock in the new status
                await self.change_presence(activity=act)
                
                await asyncio.sleep(0.5)
                await message.channel.send(msg)

            except Exception as e:
                await message.channel.send(f"❌ **{self.user.name}** Failed to update presence: {e}")

        elif command == "help":
            # STAGGER MATH: All 8 bots respond, staggered by 1 second so Discord doesn't block them!
            stagger = (self.user.id % 8 * 1.0) + random.uniform(0.1, 0.4)
            await asyncio.sleep(stagger)

            # Stage 1: Infiltration & GC Ops
            help_panel_part1 = textwrap.dedent(f"""```yaml
🔥 FORB1D OPS | MASTER CONTROL (1/2) 🔥
======================================
"Dominate the network. Engineered by FORB1D🔥"

[ 📡 INFILTRATION & EXTRACTION ]
> ^serverjoin <link>    (Swarm joins)
> ^serverjoin @bot      (Precision join)
> ^serverleave <link>   (Swarm leaves)
> ^serverleave @bot     (Precision leave)
> ^ping                 (Live latency)
> ^unping               (Stop latency)
> ^reset                (Refresh Script)

[ 👥 GROUP CHAT OPS ]
> ^gcjoin <link>        (Join GC via Link)
> ^gcnc <name> <delay>  (GC Name Flasher)
> ^ungcnc               (Stop flasher)
> ^gcleave              (Leave This GC)
> ^gcleave all          (Leave ALL GCs)
> ^gcleaveall @bot      (All GC Wipe)
> ^gcleave @bot         (Precision Leave)
> ^sgcnc <text> @userx  (Fastest GCNC)
> ^unsgcnc @user        (Remove SGCNC)
> ^gcspamall <text>     (Spam Every GC)
> ^gcncall <text>       (GCNC Every GC)
> ^ungcspamall          (Stop GC Spam)
> ^ungcncall            (Stop All GCNC)
> ^gccall               (Spam Call GC)
> ^ungccall             (Stop Spam Calls)
> ^gccreate @bot @user  (GC Creation)
> ^ungccreate           (Stop Creation)
> ^gcremoveall @users   (Remove From ALL)

======================================
⚡ Powered by FORB1D🔥 Network ⚡
[ {self.user.name} - System Online ]
```""")

            # Stage 2: Targeting & Presence
            help_panel_part2 = textwrap.dedent(f"""```yaml
🔥 FORB1D OPS | MASTER CONTROL (2/2) 🔥
======================================
[ 🎯 TARGETING & SPAM OPS ]
> ^loud @user           (Loud On User)
> ^unloud               (Stop Loud)
> ^autoreact @user 💀   (Reactors)
> ^unautoreact          (Remove Reactors)
> ^unautoreact @user    (Unlock @user)
> ^rs <text> <delay>    (Roast Spam)
> ^cs <text> <delay>    (Custom Spam)
> ^fs <text> <delay>    (Forward Spam)
> ^sspam <text> @user1  (Fast Smart Spam)
> ^unsspam @user        (Stop Smart Spam)
> ^unspam               (Stop All Spam)
> ^slide @u1 @u2        (Auto Roaster)
> ^unslide @u1 @u2      (Precise Remove)

[ 🎭 FLEX & PRESENCE OPS ]
> ^grant @user          (Grant Access)
> ^ungrant @user        (Revoke Access)
> ^presence <md> <msg>  (Set Status)
> ^stream <text>        (Purple Stream)
> ^stream stop          (Wipe Stream)
> ^rgbstream <txt> <d>  (RGB Stream)
> ^unrgbstream          (Stop RGB)
> ^recon @user          (Acc Info)
> ^purge @bot <amt>     (Del Msgs)
> ^say @bot <text>      (Bot Speak)
> ^quest all            (Swarm Autoplay)
> ^quest @bot           (Precision Quest)

======================================
⚡ Powered by FORB1D🔥 Network ⚡
[ {self.user.name} - System Online ]
```""")

            try:
                await message.channel.send(help_panel_part1)
                await asyncio.sleep(0.3)
                await message.channel.send(help_panel_part2)
            except Exception as e:
                print(f"❌ [{self.user.name}] Help Panel failed: {e}", flush=True)
       
    async def ram_cleaner_loop(self):
        import gc
        await self.wait_until_ready()
        if self.user.id % 8 != 0:
            return
        while not self.is_closed():
            try:
                await asyncio.sleep(600)
                collected = gc.collect()
                for channel_id in list(spam_tasks.keys()):
                    if channel_id in spam_tasks and not spam_tasks[channel_id]:
                        del spam_tasks[channel_id]
                for channel_id in list(gcnc_tasks.keys()):
                    if channel_id in gcnc_tasks and not gcnc_tasks[channel_id]:
                        del gcnc_tasks[channel_id]
                print(f"🧹 [Memory Engine] Deep RAM Purge complete. Freed {collected} dead objects.", flush=True)
            except Exception as e:
                print(f"⚠️ [Memory Engine] Purge failed: {e}", flush=True)

# 🛑 PASTE IT RIGHT HERE AT THE ABSOLUTE BOTTOM OF THE CLASS 🛑
    async def close(self):
        if self.raw_session:
            await self.raw_session.close()
        await super().close()
                
# 4. Master Engine Initialization
async def main():
    raw_tokens = os.environ.get('BOT_TOKENS')
    if not raw_tokens:
        print("❌ ERROR: No BOT_TOKENS found in Render Environment Variables!", flush=True)
        return

    token_list = [t.strip() for t in raw_tokens.split(',') if t.strip()]
    clients = []

    print(f"⚡ Initializing multi-token array with {len(token_list)} targets...", flush=True)

    # Create a shielded login function so dead tokens don't crash the good ones
    async def safe_start(client, token):
        try:
            await client.start(token)
        except Exception as e:
            print(f"💀 DEAD TOKEN SKIPPED [{token[:10]}...]: {e}", flush=True)

    # Build client instances for every token
    for i, token in enumerate(token_list):
        client = ForbidToken()
        clients.append(safe_start(client, token))
        
        if i < len(token_list) - 1:
            # FAST_BOOT = True gives a safe minimum 1s delay locally.
            # FAST_BOOT = False gives the full 15s+ IP cloak for Railway production.
            boot_delay = 1.0 if FAST_BOOT else (15.0 + random.uniform(1.0, 5.0))
            print(f"⏳ [System] Holding next token for {boot_delay:.1f}s...", flush=True)
            await asyncio.sleep(boot_delay)

    # Fire all connections concurrently (they are already mathematically spaced out now!)
    print("🚀 Firing connections concurrently...", flush=True)
    await asyncio.gather(*clients)
    
if __name__ == "__main__":
    # 1. Start the web server in the background ONLY after everything is loaded
    keep_alive()
    
    # 2. Ignite the botnet
    asyncio.run(main())
