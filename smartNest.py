import flet as ft
from datetime import datetime

class SmartHomeApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "SmartHome"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.padding = 0
        self.page.bgcolor = "#0f1419"
        
        # App state
        self.current_view = "dashboard"
        self.user_name = "Jordan Smith"
        self.user_email = "jordan.smith@example.com"
        
        # Device states
        self.devices = {
            "living_room_light": {"status": "ON", "brightness": 75, "color_temp": 4000},
            "bedroom_light": {"status": "OFF", "brightness": 50, "color_temp": 3000},
            "front_door": {"status": "ON", "locked": False},
            "thermostat": {"status": "Heating", "current": 21, "target": 22, "mode": "heat", "fan": "auto"},
            "ceiling_fan": {"status": "OFF", "speed": 2}
        }
        
        # Scenes
        self.scenes = [
            {"name": "Movie Night", "actions": 2, "devices": ["light1: off", "thermostat: set (21)"]},
            {"name": "Good Morning", "actions": 3, "devices": ["light1: on", "light2: on", "thermostat: set (23)"]},
            {"name": "Away Mode", "actions": 4, "devices": ["light1: off", "light2: off", "door1: lock", "thermostat: set (18)"]}
        ]
        
        self.main_content = ft.Container()
        self.build_ui()
    
    def build_ui(self):
        # Sidebar
        sidebar = ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.HOME, color=ft.Colors.BLUE_400, size=24),
                        ft.Text("SmartHome", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
                    ]),
                    padding=20
                ),
                ft.Container(height=20),
                self.create_nav_item(ft.Icons.DASHBOARD, "Dashboard", "dashboard"),
                self.create_nav_item(ft.Icons.MEETING_ROOM, "Rooms", "rooms"),
                self.create_nav_item(ft.Icons.LIGHTBULB_OUTLINE, "Scenes", "scenes"),
                self.create_nav_item(ft.Icons.AUTO_MODE, "Automations", "automations"),
                ft.Container(expand=True),
                self.create_nav_item(ft.Icons.SETTINGS, "Settings", "settings"),
                self.create_nav_item(ft.Icons.PERSON, "Profile", "profile", selected=False),
                self.create_nav_item(ft.Icons.LOGOUT, "Logout", "logout"),
            ], spacing=0),
            width=220,
            bgcolor="#1a1f2e",
            padding=ft.padding.only(top=10, bottom=10)
        )
        
        # Main layout
        layout = ft.Row([
            sidebar,
            ft.Container(
                content=self.main_content,
                expand=True,
                padding=30,
                bgcolor="#0f1419"
            )
        ], spacing=0, expand=True)
        
        self.page.add(layout)
        self.show_dashboard()
    
    def create_nav_item(self, icon, text, view_name, selected=False):
        is_selected = self.current_view == view_name
        
        def on_click(e):
            self.current_view = view_name
            if view_name == "dashboard":
                self.show_dashboard()
            elif view_name == "profile":
                self.show_profile()
            elif view_name == "scenes":
                self.show_scenes()
            elif view_name == "rooms":
                self.show_statistics()
            self.page.update()
        
        return ft.Container(
            content=ft.Row([
                ft.Icon(icon, color=ft.Colors.WHITE if is_selected else ft.Colors.GREY_400, size=20),
                ft.Text(text, color=ft.Colors.WHITE if is_selected else ft.Colors.GREY_400, size=14)
            ], spacing=15),
            padding=ft.padding.only(left=20, right=20, top=12, bottom=12),
            bgcolor=ft.Colors.BLUE_700 if is_selected else None,
            border_radius=8,
            margin=ft.margin.only(left=10, right=10),
            on_click=on_click,
            ink=True
        )

    def show_dashboard(self):
        """Main dashboard view with all devices"""
        self.main_content.content = ft.Column([
            # On/Off Devices Section
            ft.Text("On/Off Devices", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            ft.Container(height=20),
            ft.Row([
                self.create_device_card(
                    "Living Room Light",
                    "living_room_light",
                    ft.Colors.YELLOW_100,
                    ft.Icons.LIGHTBULB,
                    ft.Colors.YELLOW_700,
                    "light"
                ),
                self.create_device_card(
                    "Bedroom Light",
                    "bedroom_light",
                    ft.Colors.YELLOW_100,
                    ft.Icons.LIGHTBULB,
                    ft.Colors.YELLOW_700,
                    "light"
                ),
                self.create_device_card(
                    "Front Door",
                    "front_door",
                    ft.Colors.BLUE_100,
                    ft.Icons.DOOR_SLIDING,
                    ft.Colors.BLUE_700,
                    "door"
                ),
            ], spacing=20),
            
            ft.Container(height=30),
            
            # Slider Controlled Devices
            ft.Text("Slider Controlled Devices", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            ft.Container(height=20),
            ft.Row([
                self.create_thermostat_card(),
                self.create_fan_card(),
            ], spacing=20),
            
            ft.Container(height=30),
            
            # Scenes & Automation
            ft.Text("Scenes & Automation", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            ft.Container(height=20),
            ft.Row([
                self.create_scene_card("Movie Night", 2),
                self.create_scene_card("Good Morning", 3),
                self.create_scene_card("Away Mode", 4),
            ], spacing=20),
            
            ft.Container(height=30),
            
            # Energy Monitor
            ft.Text("Energy Monitor", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            ft.Container(height=20),
            self.create_energy_monitor(),
        ], scroll=ft.ScrollMode.AUTO)
        
        self.page.update()
    
    def create_device_card(self, name, device_id, bg_color, icon, icon_color, device_type):
        device = self.devices[device_id]
        is_on = device["status"] == "ON"
        
        def toggle_device(e):
            self.devices[device_id]["status"] = "OFF" if is_on else "ON"
            self.show_dashboard()
        
        def show_details(e):
            if device_type == "light":
                self.show_light_details(device_id, name)
        
        action_text = "Turn OFF" if is_on else "Turn ON"
        if device_type == "door":
            action_text = "Unlock" if device["locked"] else "Lock"
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Container(
                        content=ft.Icon(icon, color=icon_color, size=30),
                        width=60,
                        height=60,
                        bgcolor=ft.Colors.WHITE,
                        border_radius=30,
                        alignment=ft.alignment.center
                    ),
                    ft.Column([
                        ft.Text(name, size=16, weight=ft.FontWeight.BOLD, color="#1a1f2e"),
                        ft.Text(f"Status: {device['status']}", size=12, color="#1a1f2e"),
                        ft.Text(f"Tap to turn {'off' if is_on else 'on'}", size=10, color="#666"),
                    ], spacing=2, expand=True)
                ], spacing=15),
                ft.Container(height=15),
                ft.Row([
                    ft.TextButton("Details", on_click=show_details, style=ft.ButtonStyle(color="#5b4fc7")),
                    ft.Container(expand=True),
                    ft.ElevatedButton(
                        action_text,
                        on_click=toggle_device,
                        bgcolor="#1a1f2e",
                        color=ft.Colors.WHITE,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20))
                    )
                ])
            ], spacing=10),
            width=300,
            padding=20,
            bgcolor=bg_color,
            border_radius=15
        )

    def create_thermostat_card(self):
        device = self.devices["thermostat"]
        
        def on_slider_change(e):
            self.devices["thermostat"]["target"] = int(e.control.value)
            temp_text.value = f"{int(e.control.value)}°C"
            self.page.update()
        
        def show_details(e):
            self.show_thermostat_details()
        
        temp_text = ft.Text(f"{device['target']}°C", size=12, color="#8b5a5a")
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.Icons.THERMOSTAT, color=ft.Colors.RED_400, size=30),
                        width=60,
                        height=60,
                        bgcolor=ft.Colors.WHITE,
                        border_radius=30,
                        alignment=ft.alignment.center
                    ),
                    ft.Column([
                        ft.Text("Thermostat", size=16, weight=ft.FontWeight.BOLD, color="#8b5a5a"),
                        ft.Text(f"Set point: {device['target']}°C", size=12, color="#8b5a5a"),
                        ft.Text("Use slider to change", size=10, color="#a88"),
                    ], spacing=2, expand=True)
                ], spacing=15),
                ft.Container(height=10),
                ft.Row([
                    ft.Icon(ft.Icons.AC_UNIT, color=ft.Colors.BLUE_300, size=20),
                    ft.Slider(
                        min=15,
                        max=30,
                        value=device['target'],
                        on_change=on_slider_change,
                        active_color=ft.Colors.BLUE_400,
                        thumb_color=ft.Colors.BLUE_600,
                        expand=True
                    ),
                    ft.Icon(ft.Icons.LOCAL_FIRE_DEPARTMENT, color=ft.Colors.RED_300, size=20),
                ], spacing=10),
                temp_text,
                ft.TextButton("Details", on_click=show_details, style=ft.ButtonStyle(color="#8b5a5a"))
            ], spacing=10),
            width=450,
            padding=20,
            bgcolor="#ffe5e5",
            border_radius=15
        )
    
    def create_fan_card(self):
        device = self.devices["ceiling_fan"]
        
        def on_slider_change(e):
            self.devices["ceiling_fan"]["speed"] = int(e.control.value)
            speed_text.value = f"Fan speed: {int(e.control.value)}"
            self.page.update()
        
        speed_text = ft.Text(f"Fan speed: {device['speed']}", size=12, color="#4a7c7c")
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.Icons.AIR, color=ft.Colors.CYAN_600, size=30),
                        width=60,
                        height=60,
                        bgcolor=ft.Colors.WHITE,
                        border_radius=30,
                        alignment=ft.alignment.center
                    ),
                    ft.Column([
                        ft.Text("Ceiling Fan", size=16, weight=ft.FontWeight.BOLD, color="#4a7c7c"),
                        ft.Text(f"Fan speed: {device['speed']}", size=12, color="#4a7c7c"),
                        ft.Text("0 = OFF, 3 = MAX", size=10, color="#6aa"),
                    ], spacing=2, expand=True)
                ], spacing=15),
                ft.Container(height=10),
                ft.Slider(
                    min=0,
                    max=3,
                    divisions=3,
                    value=device['speed'],
                    on_change=on_slider_change,
                    active_color=ft.Colors.CYAN_400,
                    thumb_color=ft.Colors.CYAN_600
                ),
                speed_text,
                ft.TextButton("Details", style=ft.ButtonStyle(color="#4a7c7c"))
            ], spacing=10),
            width=450,
            padding=20,
            bgcolor="#d4f4f4",
            border_radius=15
        )
    
    def create_scene_card(self, name, device_count):
        def activate_scene(e):
            # Scene activation logic
            pass
        
        return ft.Container(
            content=ft.Column([
                ft.Text(name, size=18, weight=ft.FontWeight.BOLD, color="#1a1f2e"),
                ft.Text(f"{device_count} devices", size=12, color="#666"),
                ft.Container(height=10),
                ft.ElevatedButton(
                    "▶ Activate Scene",
                    on_click=activate_scene,
                    bgcolor="#7c3aed",
                    color=ft.Colors.WHITE,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20))
                )
            ], spacing=5, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=280,
            padding=20,
            bgcolor="#f3f4f6",
            border_radius=15,
            alignment=ft.alignment.center
        )
    
    def create_energy_monitor(self):
        return ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.BOLT, color=ft.Colors.YELLOW_700, size=40),
                ft.Column([
                    ft.Text("Current Power Usage", size=14, color="#666"),
                    ft.Text("65 W", size=36, weight=ft.FontWeight.BOLD, color=ft.Colors.YELLOW_700),
                    ft.Text("Estimated cost: $0.19/day", size=12, color="#666"),
                ], spacing=5)
            ], spacing=20),
            padding=30,
            bgcolor="#fffbeb",
            border_radius=15
        )

    def show_profile(self):
        """Profile page with account settings"""
        def save_changes(e):
            self.user_name = name_field.value
            self.user_email = email_field.value
            self.page.show_snack_bar(ft.SnackBar(content=ft.Text("Changes saved successfully!")))
        
        name_field = ft.TextField(
            label="Full Name",
            value=self.user_name,
            bgcolor="#1a2332",
            border_color="#2a3342",
            color=ft.Colors.WHITE
        )
        
        email_field = ft.TextField(
            label="Email Address",
            value=self.user_email,
            bgcolor="#1a2332",
            border_color="#2a3342",
            color=ft.Colors.WHITE
        )
        
        self.main_content.content = ft.Column([
            # Header with profile
            ft.Row([
                ft.Container(
                    content=ft.Text(
                        self.user_name[0].upper(),
                        size=40,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE
                    ),
                    width=100,
                    height=100,
                    bgcolor=ft.Colors.with_opacity(0.3, ft.Colors.TEAL_400),
                    border_radius=50,
                    alignment=ft.alignment.center
                ),
                ft.Column([
                    ft.Text(self.user_name, size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Text("Member since Jan 2023", size=14, color=ft.Colors.GREY_400),
                ], spacing=5),
                ft.Container(expand=True),
                ft.ElevatedButton(
                    "Edit Profile",
                    bgcolor=ft.Colors.BLUE_600,
                    color=ft.Colors.WHITE,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                )
            ], alignment=ft.MainAxisAlignment.START),
            
            ft.Container(height=30),
            
            # Stats cards
            ft.Row([
                self.create_stat_card("Active Devices", "15", "#1e3a5f"),
                self.create_stat_card("Scenes Created", "8", "#1e3a5f"),
                self.create_stat_card("Energy Saved", "12 kWh", "#1e3a5f"),
                self.create_stat_card("Most Used", "Living Room", "#1e3a5f"),
            ], spacing=20),
            
            ft.Container(height=30),
            
            # Tabs section
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.TextButton("Account Details", style=ft.ButtonStyle(color=ft.Colors.BLUE_400)),
                        ft.TextButton("Notifications", style=ft.ButtonStyle(color=ft.Colors.GREY_400)),
                        ft.TextButton("Dashboard Customization", style=ft.ButtonStyle(color=ft.Colors.GREY_400)),
                    ]),
                    ft.Divider(color="#2a3342", height=1),
                    
                    ft.Container(height=20),
                    
                    # Account Details Form
                    ft.Row([
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Full Name", size=14, color=ft.Colors.GREY_400),
                                name_field
                            ], spacing=10),
                            expand=True
                        ),
                        ft.Container(width=20),
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Email Address", size=14, color=ft.Colors.GREY_400),
                                email_field
                            ], spacing=10),
                            expand=True
                        ),
                    ]),
                    
                    ft.Container(height=30),
                    
                    # Change Password
                    ft.Container(
                        content=ft.Row([
                            ft.Column([
                                ft.Text("Change Password", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                                ft.Text("Set a new password for your account.", size=12, color=ft.Colors.GREY_400),
                            ], spacing=5),
                            ft.Container(expand=True),
                            ft.OutlinedButton(
                                "Change Password",
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    side=ft.BorderSide(1, ft.Colors.GREY_600)
                                )
                            )
                        ]),
                        padding=20,
                        border=ft.border.all(1, "#2a3342"),
                        border_radius=8
                    ),
                    
                    ft.Container(height=20),
                    
                    # Two-Factor Authentication
                    ft.Container(
                        content=ft.Row([
                            ft.Column([
                                ft.Text("Two-Factor Authentication", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                                ft.Text("Add an extra layer of security.", size=12, color=ft.Colors.GREY_400),
                            ], spacing=5),
                            ft.Container(expand=True),
                            ft.OutlinedButton(
                                "Enable 2FA",
                                style=ft.ButtonStyle(
                                    color=ft.Colors.WHITE,
                                    side=ft.BorderSide(1, ft.Colors.GREY_600)
                                )
                            )
                        ]),
                        padding=20,
                        border=ft.border.all(1, "#2a3342"),
                        border_radius=8
                    ),
                    
                    ft.Container(height=20),
                    ft.Divider(color="#2a3342", height=1),
                    ft.Container(height=20),
                    
                    # Delete Account
                    ft.Container(
                        content=ft.Row([
                            ft.Column([
                                ft.Text("Delete Account", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.RED_400),
                                ft.Text("Permanently remove your account and all data.", size=12, color=ft.Colors.GREY_400),
                            ], spacing=5),
                            ft.Container(expand=True),
                            ft.ElevatedButton(
                                "Delete My Account",
                                bgcolor=ft.Colors.RED_900,
                                color=ft.Colors.RED_400,
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                            )
                        ]),
                        padding=20,
                    ),
                    
                    ft.Container(height=20),
                    
                    # Save button
                    ft.Row([
                        ft.Container(expand=True),
                        ft.ElevatedButton(
                            "Save Changes",
                            on_click=save_changes,
                            bgcolor=ft.Colors.BLUE_600,
                            color=ft.Colors.WHITE,
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                        )
                    ])
                ], spacing=0),
                padding=30,
                bgcolor="#1a2332",
                border_radius=15
            )
        ], scroll=ft.ScrollMode.AUTO)
        
        self.page.update()
    
    def create_stat_card(self, label, value, bg_color):
        return ft.Container(
            content=ft.Column([
                ft.Text(label, size=12, color=ft.Colors.GREY_400),
                ft.Text(value, size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            ], spacing=5, horizontal_alignment=ft.CrossAxisAlignment.START),
            padding=20,
            bgcolor=bg_color,
            border_radius=12,
            expand=True
        )

    def show_thermostat_details(self):
        """Detailed thermostat control page"""
        device = self.devices["thermostat"]
        
        def back_to_dashboard(e):
            self.show_dashboard()
        
        def set_mode(mode):
            def handler(e):
                self.devices["thermostat"]["mode"] = mode
                self.show_thermostat_details()
            return handler
        
        def set_fan_mode(mode):
            def handler(e):
                self.devices["thermostat"]["fan"] = mode
                self.show_thermostat_details()
            return handler
        
        def on_temp_change(e):
            self.devices["thermostat"]["target"] = int(e.control.value)
            target_temp_text.value = f"{int(e.control.value)}°C"
            self.page.update()
        
        target_temp_text = ft.Text(f"{device['target']}°C", size=14, color=ft.Colors.GREY_400)
        
        # Mode buttons
        mode_buttons = ft.Row([
            self.create_mode_button("Heat", ft.Icons.LOCAL_FIRE_DEPARTMENT, "heat", device["mode"], set_mode("heat")),
            self.create_mode_button("Cool", ft.Icons.AC_UNIT, "cool", device["mode"], set_mode("cool")),
            self.create_mode_button("Auto", ft.Icons.AUTORENEW, "auto", device["mode"], set_mode("auto")),
        ], spacing=15)
        
        # Fan buttons
        fan_buttons = ft.Row([
            self.create_mode_button("Auto", ft.Icons.AIR, "auto", device["fan"], set_fan_mode("auto")),
            self.create_mode_button("Off", ft.Icons.POWER_SETTINGS_NEW, "off", device["fan"], set_fan_mode("off")),
            self.create_mode_button("On", ft.Icons.AIR, "on", device["fan"], set_fan_mode("on")),
        ], spacing=15)
        
        self.main_content.content = ft.Column([
            # Header
            ft.Row([
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    on_click=back_to_dashboard,
                    icon_color=ft.Colors.WHITE
                ),
                ft.Text("Back to Dashboard", size=14, color=ft.Colors.GREY_400),
            ]),
            
            ft.Container(height=20),
            
            # Device header
            ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.THERMOSTAT, color=ft.Colors.BLUE_400, size=30),
                    width=60,
                    height=60,
                    bgcolor=ft.Colors.BLUE_900,
                    border_radius=30,
                    alignment=ft.alignment.center
                ),
                ft.Column([
                    ft.Text("Smart Thermostat", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Text(f"Status: {device['status']} • Set to {device['target']}°C", 
                           size=14, color=ft.Colors.GREY_400),
                ], spacing=5),
                ft.Container(expand=True),
                ft.Row([
                    ft.IconButton(icon=ft.Icons.SETTINGS, icon_color=ft.Colors.WHITE),
                    ft.ElevatedButton(
                        "Turn OFF",
                        bgcolor="#1a2332",
                        color=ft.Colors.WHITE,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20))
                    )
                ])
            ]),
            
            ft.Container(height=30),
            
            # Main content
            ft.Row([
                # Controls section
                ft.Container(
                    content=ft.Column([
                        ft.Text("Controls", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                        ft.Container(height=20),
                        
                        # Temperature circle
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Current", size=12, color=ft.Colors.GREY_400),
                                ft.Text(f"{device['current']}°", size=48, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            width=200,
                            height=200,
                            border=ft.border.all(8, ft.Colors.BLUE_600),
                            border_radius=100,
                            alignment=ft.alignment.center
                        ),
                        
                        ft.Container(height=30),
                        
                        # Temperature slider
                        ft.Column([
                            ft.Row([
                                ft.Text("Target Temperature", size=14, color=ft.Colors.WHITE),
                                ft.Container(expand=True),
                                target_temp_text
                            ]),
                            ft.Row([
                                ft.Icon(ft.Icons.AC_UNIT, color=ft.Colors.BLUE_300, size=20),
                                ft.Slider(
                                    min=15,
                                    max=30,
                                    value=device['target'],
                                    on_change=on_temp_change,
                                    active_color=ft.Colors.BLUE_400,
                                    thumb_color=ft.Colors.BLUE_600,
                                    expand=True
                                ),
                                ft.Icon(ft.Icons.LOCAL_FIRE_DEPARTMENT, color=ft.Colors.RED_300, size=20),
                            ])
                        ], spacing=10),
                        
                        ft.Container(height=30),
                        
                        # Mode selection
                        ft.Column([
                            ft.Text("Mode", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                            ft.Container(height=10),
                            mode_buttons
                        ]),
                        
                        ft.Container(height=20),
                        
                        # Fan selection
                        ft.Column([
                            ft.Text("Fan", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                            ft.Container(height=10),
                            fan_buttons
                        ]),
                    ], spacing=10),
                    padding=30,
                    bgcolor="#1a2332",
                    border_radius=15,
                    expand=True
                ),
                
                ft.Container(width=20),
                
                # Right sidebar
                ft.Column([
                    # Schedule
                    ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Text("Schedule", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                                ft.Container(expand=True),
                                ft.IconButton(icon=ft.Icons.ADD, icon_color=ft.Colors.BLUE_400, icon_size=20)
                            ]),
                            ft.Container(height=15),
                            self.create_schedule_item("Morning (22°C)", "7:00 AM", True),
                            self.create_schedule_item("Night (20°C)", "11:00 PM", True),
                        ], spacing=10),
                        padding=20,
                        bgcolor="#1a2332",
                        border_radius=15,
                        width=300
                    ),
                    
                    ft.Container(height=20),
                    
                    # Information
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Information", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                            ft.Container(height=15),
                            self.create_info_row("Device Model", "ThermoSmart X"),
                            self.create_info_row("Firmware", "v3.1.2"),
                            self.create_info_row("MAC Address", "A1:B2:C3:D4:E5:F6"),
                            self.create_info_row("Uptime", "12d 4h 8m"),
                        ], spacing=10),
                        padding=20,
                        bgcolor="#1a2332",
                        border_radius=15,
                        width=300
                    ),
                ]),
            ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.START),
            
            ft.Container(height=30),
            
            # Usage History
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text("Usage History", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                        ft.Container(expand=True),
                        ft.Dropdown(
                            value="Last 7 Days",
                            options=[
                                ft.dropdown.Option("Last 7 Days"),
                                ft.dropdown.Option("Last 30 Days"),
                                ft.dropdown.Option("Last 3 Months"),
                            ],
                            width=150,
                            bgcolor="#0f1419",
                            border_color="#2a3342"
                        )
                    ]),
                    ft.Container(height=20),
                    ft.Container(
                        content=ft.Text("Chart Data Here", size=14, color=ft.Colors.GREY_600),
                        height=200,
                        alignment=ft.alignment.center,
                        bgcolor="#0f1419",
                        border_radius=8
                    )
                ], spacing=10),
                padding=30,
                bgcolor="#1a2332",
                border_radius=15
            )
        ], scroll=ft.ScrollMode.AUTO)
        
        self.page.update()

    def show_light_details(self, device_id, device_name):
        """Detailed light control page"""
        device = self.devices[device_id]
        
        def back_to_dashboard(e):
            self.show_dashboard()
        
        def toggle_light(e):
            self.devices[device_id]["status"] = "OFF" if device["status"] == "ON" else "ON"
            self.show_light_details(device_id, device_name)
        
        def on_brightness_change(e):
            self.devices[device_id]["brightness"] = int(e.control.value)
            brightness_text.value = f"{int(e.control.value)}%"
            self.page.update()
        
        def on_color_temp_change(e):
            self.devices[device_id]["color_temp"] = int(e.control.value)
            temp_text.value = f"{int(e.control.value)}K"
            self.page.update()
        
        brightness_text = ft.Text(f"{device['brightness']}%", size=14, color=ft.Colors.GREY_400)
        temp_text = ft.Text(f"{device['color_temp']}K", size=14, color=ft.Colors.GREY_400)
        
        self.main_content.content = ft.Column([
            # Header
            ft.Row([
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    on_click=back_to_dashboard,
                    icon_color=ft.Colors.WHITE
                ),
                ft.Text("Back to Dashboard", size=14, color=ft.Colors.GREY_400),
            ]),
            
            ft.Container(height=20),
            
            # Device header
            ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.LIGHTBULB, color=ft.Colors.YELLOW_600, size=30),
                    width=60,
                    height=60,
                    bgcolor=ft.Colors.YELLOW_900,
                    border_radius=30,
                    alignment=ft.alignment.center
                ),
                ft.Column([
                    ft.Text(device_name, size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Text(f"Status: {device['status']} • {device['brightness']}% Brightness", 
                           size=14, color=ft.Colors.GREY_400),
                ], spacing=5),
                ft.Container(expand=True),
                ft.Row([
                    ft.IconButton(icon=ft.Icons.SETTINGS, icon_color=ft.Colors.WHITE),
                    ft.ElevatedButton(
                        "Turn OFF" if device["status"] == "ON" else "Turn ON",
                        on_click=toggle_light,
                        bgcolor="#1a2332",
                        color=ft.Colors.WHITE,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20))
                    )
                ])
            ]),
            
            ft.Container(height=30),
            
            # Main content
            ft.Row([
                # Controls section
                ft.Container(
                    content=ft.Column([
                        ft.Text("Controls", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                        ft.Container(height=30),
                        
                        # Brightness control
                        ft.Column([
                            ft.Row([
                                ft.Text("Brightness", size=16, color=ft.Colors.WHITE),
                                ft.Container(expand=True),
                                brightness_text
                            ]),
                            ft.Container(height=10),
                            ft.Row([
                                ft.Icon(ft.Icons.LIGHTBULB_OUTLINE, color=ft.Colors.GREY_400, size=20),
                                ft.Slider(
                                    min=0,
                                    max=100,
                                    value=device['brightness'],
                                    on_change=on_brightness_change,
                                    active_color=ft.Colors.BLUE_400,
                                    thumb_color=ft.Colors.BLUE_600,
                                    expand=True
                                ),
                                ft.Icon(ft.Icons.LIGHTBULB, color=ft.Colors.YELLOW_600, size=20),
                            ])
                        ], spacing=5),
                        
                        ft.Container(height=30),
                        
                        # Color Temperature control
                        ft.Column([
                            ft.Row([
                                ft.Text("Color Temperature", size=16, color=ft.Colors.WHITE),
                                ft.Container(expand=True),
                                temp_text
                            ]),
                            ft.Container(height=10),
                            ft.Row([
                                ft.Icon(ft.Icons.WB_SUNNY, color=ft.Colors.ORANGE_400, size=20),
                                ft.Container(
                                    content=ft.Slider(
                                        min=2000,
                                        max=6500,
                                        value=device['color_temp'],
                                        on_change=on_color_temp_change,
                                        thumb_color=ft.Colors.BLUE_600,
                                        expand=True
                                    ),
                                    gradient=ft.LinearGradient(
                                        begin=ft.alignment.center_left,
                                        end=ft.alignment.center_right,
                                        colors=[ft.Colors.ORANGE_400, ft.Colors.YELLOW_300, ft.Colors.BLUE_200]
                                    ),
                                    border_radius=10,
                                    padding=5,
                                    expand=True
                                ),
                                ft.Icon(ft.Icons.AC_UNIT, color=ft.Colors.BLUE_300, size=20),
                            ])
                        ], spacing=5),
                    ], spacing=10),
                    padding=30,
                    bgcolor="#1a2332",
                    border_radius=15,
                    expand=True
                ),
                
                ft.Container(width=20),
                
                # Right sidebar
                ft.Column([
                    # Schedule
                    ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Text("Schedule", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                                ft.Container(expand=True),
                                ft.IconButton(icon=ft.Icons.ADD, icon_color=ft.Colors.BLUE_400, icon_size=20)
                            ]),
                            ft.Container(height=15),
                            self.create_schedule_item("ON - Weekdays", "7:00 AM", True),
                            self.create_schedule_item("OFF - Everyday", "11:00 PM", True),
                        ], spacing=10),
                        padding=20,
                        bgcolor="#1a2332",
                        border_radius=15,
                        width=300
                    ),
                    
                    ft.Container(height=20),
                    
                    # Information
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Information", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                            ft.Container(height=15),
                            self.create_info_row("Device Model", "SmartColor A19"),
                            self.create_info_row("Firmware", "v2.5.1"),
                            self.create_info_row("MAC Address", "1A:2B:3C:4D:5E:6F"),
                            self.create_info_row("Uptime", "3d 14h 22m"),
                        ], spacing=10),
                        padding=20,
                        bgcolor="#1a2332",
                        border_radius=15,
                        width=300
                    ),
                ]),
            ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.START),
            
            ft.Container(height=30),
            
            # Usage History
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text("Usage History", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                        ft.Container(expand=True),
                        ft.Dropdown(
                            value="Last 7 Days",
                            options=[
                                ft.dropdown.Option("Last 7 Days"),
                                ft.dropdown.Option("Last 30 Days"),
                            ],
                            width=150,
                            bgcolor="#0f1419",
                            border_color="#2a3342"
                        )
                    ]),
                    ft.Container(height=20),
                    ft.Container(
                        content=ft.Text("Chart Data Here", size=14, color=ft.Colors.GREY_600),
                        height=200,
                        alignment=ft.alignment.center,
                        bgcolor="#0f1419",
                        border_radius=8
                    )
                ], spacing=10),
                padding=30,
                bgcolor="#1a2332",
                border_radius=15
            )
        ], scroll=ft.ScrollMode.AUTO)
        
        self.page.update()
    
    def create_mode_button(self, text, icon, mode_value, current_mode, on_click):
        is_selected = current_mode == mode_value
        return ft.Container(
            content=ft.Column([
                ft.Icon(icon, color=ft.Colors.ORANGE_400 if is_selected else ft.Colors.GREY_400, size=24),
                ft.Text(text, size=12, color=ft.Colors.WHITE if is_selected else ft.Colors.GREY_400)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
            width=90,
            height=80,
            bgcolor=ft.Colors.BLUE_900 if is_selected else "#0f1419",
            border_radius=8,
            alignment=ft.alignment.center,
            on_click=on_click,
            border=ft.border.all(2, ft.Colors.BLUE_600 if is_selected else "#2a3342")
        )
    
    def create_schedule_item(self, title, time, enabled):
        return ft.Row([
            ft.Column([
                ft.Text(title, size=14, color=ft.Colors.WHITE),
                ft.Text(time, size=12, color=ft.Colors.GREY_400),
            ], spacing=2),
            ft.Container(expand=True),
            ft.Switch(value=enabled, active_color=ft.Colors.BLUE_600)
        ])
    
    def create_info_row(self, label, value):
        return ft.Row([
            ft.Text(label, size=12, color=ft.Colors.GREY_400),
            ft.Container(expand=True),
            ft.Text(value, size=12, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
        ])

    def show_scenes(self):
        """Scenes and automation page"""
        def create_new_scene(e):
            self.page.show_snack_bar(ft.SnackBar(content=ft.Text("Create new scene feature coming soon!")))
        
        self.main_content.content = ft.Column([
            ft.Text("Scenes & Automation", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            ft.Container(height=20),
            
            ft.Text("Your Scenes", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            ft.Container(height=15),
            
            # Scene cards
            self.create_scene_detail_card(
                "Movie Night",
                2,
                ["light1: off", "thermostat: set (21)"],
                ft.Colors.PURPLE_900
            ),
            
            ft.Container(height=15),
            
            self.create_scene_detail_card(
                "Good Morning",
                3,
                ["light1: on", "light2: on", "thermostat: set (23)"],
                ft.Colors.PURPLE_900
            ),
            
            ft.Container(height=15),
            
            self.create_scene_detail_card(
                "Away Mode",
                4,
                ["light1: off", "light2: off", "door1: lock", "thermostat: set (18)"],
                ft.Colors.PURPLE_900
            ),
            
            ft.Container(height=30),
            
            # Create new scene button
            ft.ElevatedButton(
                "+ Create New Scene",
                on_click=create_new_scene,
                bgcolor=ft.Colors.PURPLE_700,
                color=ft.Colors.WHITE,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                height=50
            )
        ], scroll=ft.ScrollMode.AUTO)
        
        self.page.update()
    
    def create_scene_detail_card(self, name, action_count, actions, bg_color):
        def activate_scene(e):
            self.page.show_snack_bar(ft.SnackBar(content=ft.Text(f"{name} activated!")))
        
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.PLAY_ARROW, color=ft.Colors.WHITE, size=24),
                    width=50,
                    height=50,
                    bgcolor=ft.Colors.PURPLE_700,
                    border_radius=25,
                    alignment=ft.alignment.center
                ),
                ft.Column([
                    ft.Text(name, size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Text(f"{action_count} actions", size=12, color=ft.Colors.GREY_400),
                    ft.Container(height=5),
                    ft.Column([
                        ft.Text(f"• {action}", size=11, color=ft.Colors.GREY_400)
                        for action in actions
                    ], spacing=2)
                ], spacing=2),
                ft.Container(expand=True),
                ft.IconButton(
                    icon=ft.Icons.CHEVRON_RIGHT,
                    icon_color=ft.Colors.WHITE,
                    on_click=activate_scene
                )
            ], alignment=ft.MainAxisAlignment.START),
            padding=20,
            bgcolor=bg_color,
            border_radius=12,
            width=None
        )
    
    def show_statistics(self):
        """Statistics and energy page"""
        self.main_content.content = ft.Column([
            ft.Text("Activity & Device Statistics", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            ft.Container(height=20),
            
            # Top stats
            ft.Row([
                self.create_large_stat_card(ft.Icons.THERMOSTAT, "21", "Total Actions", "#dbeafe"),
                self.create_large_stat_card(ft.Icons.DEVICES, "3", "Active Devices", "#d1fae5"),
                self.create_large_stat_card(ft.Icons.BOLT, "105W", "Total Power", "#fed7aa"),
            ], spacing=20),
            
            ft.Container(height=30),
            
            # Activity Over Time
            ft.Container(
                content=ft.Column([
                    ft.Text("Activity Over Time", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Container(height=20),
                    ft.Container(
                        content=ft.Column([
                            ft.Container(
                                content=ft.Container(
                                    width=80,
                                    height=200,
                                    bgcolor=ft.Colors.BLUE_600,
                                    border_radius=ft.border_radius.only(top_left=8, top_right=8)
                                ),
                                alignment=ft.alignment.bottom_center,
                                height=250
                            ),
                            ft.Text("22:00", size=10, color=ft.Colors.GREY_400)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=20,
                        bgcolor="#f9fafb",
                        border_radius=8,
                        height=300
                    )
                ]),
                padding=30,
                bgcolor="#1a2332",
                border_radius=15
            ),
            
            ft.Container(height=30),
            
            # Device Statistics
            ft.Container(
                content=ft.Column([
                    ft.Text("Device Statistics", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Container(height=20),
                    self.create_device_stat_row(ft.Icons.LIGHTBULB, "Living Room Light", "Active", "60W", ft.Colors.ORANGE_400),
                    ft.Divider(color="#2a3342"),
                    self.create_device_stat_row(ft.Icons.LIGHTBULB, "Bedroom Light", "Active", "40W", ft.Colors.ORANGE_400),
                    ft.Divider(color="#2a3342"),
                    self.create_device_stat_row(ft.Icons.DOOR_SLIDING, "Front Door", "Active", "5W", ft.Colors.GREY_400),
                    ft.Divider(color="#2a3342"),
                    self.create_device_stat_row(ft.Icons.THERMOSTAT, "Thermostat", "Inactive", "0W", ft.Colors.RED_400),
                    ft.Divider(color="#2a3342"),
                    self.create_device_stat_row(ft.Icons.AIR, "Ceiling Fan", "Inactive", "0W", ft.Colors.CYAN_400),
                ]),
                padding=30,
                bgcolor="#1a2332",
                border_radius=15
            ),
            
            ft.Container(height=30),
            
            # Action Log
            ft.Container(
                content=ft.Column([
                    ft.Text("Action Log (Last 15 Actions)", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Container(height=20),
                    ft.Container(
                        content=ft.Text("No recent actions to display.", size=14, color=ft.Colors.GREY_600),
                        height=150,
                        alignment=ft.alignment.center,
                        bgcolor="#0f1419",
                        border_radius=8
                    )
                ]),
                padding=30,
                bgcolor="#1a2332",
                border_radius=15
            ),
            
            ft.Container(height=30),
            
            # Energy Optimization
            ft.Text("Energy Optimization", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            ft.Container(height=20),
            
            ft.Row([
                self.create_energy_card(ft.Icons.BOLT, "105 W", "Current Usage", "#fef3c7"),
                self.create_energy_card(ft.Icons.ATTACH_MONEY_OUTLINED, "$0.30", "Today's Cost", "#d1fae5"),
                self.create_energy_card(ft.Icons.CALENDAR_TODAY, "$9.07", "Est. Monthly", "#dbeafe"),
            ], spacing=20),
            
            ft.Container(height=20),
            
            # Energy Saving Tips
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.LIGHTBULB_OUTLINE, color=ft.Colors.GREEN_700, size=20),
                        ft.Text("Energy Saving Tips", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_900),
                    ], spacing=10),
                    ft.Container(height=10),
                    ft.Text("• Use 'Away Mode' scene when leaving home", size=12, color=ft.Colors.GREEN_900),
                    ft.Text("• Set thermostat to 20°C at night for optimal efficiency", size=12, color=ft.Colors.GREEN_900),
                    ft.Text("• Turn off lights in unused rooms", size=12, color=ft.Colors.GREEN_900),
                    ft.Container(height=5),
                    ft.Text("• Potential savings: $1.36/month", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700),
                ], spacing=5),
                padding=20,
                bgcolor="#f0fdf4",
                border_radius=12,
                border=ft.border.all(1, ft.Colors.GREEN_200)
            ),
            
            ft.Container(height=20),
            
            # This Week vs Last Week
            ft.Container(
                content=ft.Column([
                    ft.Text("This Week vs Last Week", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Container(height=20),
                    self.create_energy_comparison_row("11/21", 20, 26),
                    self.create_energy_comparison_row("11/22", 19, 19),
                    self.create_energy_comparison_row("11/23", 21, 21),
                    self.create_energy_comparison_row("11/24", 17, 17),
                    self.create_energy_comparison_row("11/25", 22, 22),
                    self.create_energy_comparison_row("11/26", 19, 19),
                    self.create_energy_comparison_row("11/27", 16, 16),
                    ft.Container(height=10),
                    ft.Row([
                        ft.Container(width=10, height=10, bgcolor=ft.Colors.BLUE_600, border_radius=2),
                        ft.Text("Blue = This week", size=10, color=ft.Colors.GREY_400),
                        ft.Container(width=20),
                        ft.Container(width=10, height=10, bgcolor=ft.Colors.GREEN_400, border_radius=2),
                        ft.Text("Green = Last week", size=10, color=ft.Colors.GREY_400),
                    ])
                ]),
                padding=30,
                bgcolor="#1a2332",
                border_radius=15
            ),
        ], scroll=ft.ScrollMode.AUTO)
        
        self.page.update()
    
    def create_large_stat_card(self, icon, value, label, bg_color):
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(icon, color=ft.Colors.BLUE_700, size=30),
                    width=60,
                    height=60,
                    bgcolor=bg_color,
                    border_radius=30,
                    alignment=ft.alignment.center
                ),
                ft.Column([
                    ft.Text(value, size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Text(label, size=12, color=ft.Colors.GREY_400),
                ], spacing=2)
            ], spacing=15),
            padding=20,
            bgcolor="#1a2332",
            border_radius=12,
            expand=True
        )
    
    def create_device_stat_row(self, icon, name, status, power, icon_color):
        status_color = ft.Colors.GREEN_400 if status == "Active" else ft.Colors.GREY_400
        return ft.Row([
            ft.Icon(icon, color=icon_color, size=20),
            ft.Text(name, size=14, color=ft.Colors.WHITE, expand=True),
            ft.Container(
                content=ft.Text(status, size=12, color=status_color),
                padding=ft.padding.symmetric(horizontal=10, vertical=5),
                bgcolor=ft.Colors.GREEN_900 if status == "Active" else ft.Colors.GREY_800,
                border_radius=12
            ),
            ft.Text(power, size=14, color=ft.Colors.ORANGE_400, weight=ft.FontWeight.BOLD),
        ], spacing=15)
    
    def create_energy_card(self, icon, value, label, bg_color):
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(icon, color=ft.Colors.ORANGE_700, size=24),
                    width=50,
                    height=50,
                    bgcolor=bg_color,
                    border_radius=25,
                    alignment=ft.alignment.center
                ),
                ft.Column([
                    ft.Text(value, size=24, weight=ft.FontWeight.BOLD, color="#1a1f2e"),
                    ft.Text(label, size=12, color="#666"),
                ], spacing=2)
            ], spacing=15),
            padding=20,
            bgcolor=bg_color,
            border_radius=12,
            expand=True
        )
    
    def create_energy_comparison_row(self, date, this_week, last_week):
        max_width = 600
        this_week_width = (this_week / 30) * max_width
        last_week_width = (last_week / 30) * max_width
        
        return ft.Row([
            ft.Text(date, size=11, color=ft.Colors.GREY_400, width=50),
            ft.Stack([
                ft.Container(
                    width=this_week_width,
                    height=25,
                    bgcolor=ft.Colors.BLUE_600,
                    border_radius=4
                ),
                ft.Container(
                    width=last_week_width,
                    height=25,
                    bgcolor=ft.Colors.with_opacity(0.3, ft.Colors.GREEN_400),
                    border_radius=4
                ),
            ], width=max_width),
            ft.Text(f"{this_week} kWh", size=11, color=ft.Colors.WHITE, width=60),
        ], spacing=10)


def main(page: ft.Page):
    SmartHomeApp(page)

if __name__ == "__main__":
    ft.app(target=main)
