"""Premium Dark Theme Weather Application"""

import flet as ft
import asyncio
import json
from pathlib import Path
from datetime import datetime
from weather_service import WeatherService, WeatherServiceError
from config import Config


class WeatherApp:
    """Premium Dark Theme Weather Application"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.weather_service = WeatherService()
        self.history_file = Path("search_history.json")
        self.search_history = self.load_history()
        self.current_weather_data = None
        self.current_city = None
        self.setup_page()
        self.build_ui()
    
    def setup_page(self):
        """Configure page settings."""
        self.page.title = Config.APP_TITLE
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.bgcolor = "#1a1a2e"
        self.page.padding = 0
        self.page.window.width = 1000
        self.page.window.height = 720
        self.page.window.resizable = True
        self.page.window.center()
    
    def load_history(self):
        """Load search history from file."""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_history(self):
        """Save search history to file."""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.search_history, f)
        except Exception as e:
            print(f"Error saving history: {e}")
    
    def add_to_history(self, city: str):
        """Add city to search history."""
        city = city.title()
        if city in self.search_history:
            self.search_history.remove(city)
        self.search_history.insert(0, city)
        self.search_history = self.search_history[:5]
        self.save_history()
    
    def build_ui(self):
        """Build the premium dark UI."""
        # Search input
        self.city_input = ft.TextField(
            hint_text="Search for cities",
            hint_style=ft.TextStyle(color="#6b7280", size=14),
            border=ft.InputBorder.NONE,
            bgcolor="transparent",
            color="#ffffff",
            cursor_color="#ffffff",
            text_size=14,
            expand=True,
            on_submit=self.on_search,
        )
        
        # Search container
        search_container = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.SEARCH, color="#6b7280", size=20),
                    self.city_input,
                ],
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor="#252540",
            border_radius=12,
            padding=ft.padding.symmetric(horizontal=15, vertical=12),
            expand=True,
        )
        
        # Search button
        search_btn = ft.Container(
            content=ft.Icon(ft.Icons.SEARCH, color="#ffffff", size=20),
            bgcolor="#3b82f6",
            border_radius=12,
            padding=12,
            on_click=self.on_search,
            ink=True,
        )
        
        # Loading
        self.loading = ft.ProgressRing(visible=False, color="#3b82f6", width=24, height=24, stroke_width=3)
        
        # Error
        self.error_text = ft.Text("", color="#ef4444", size=13, visible=False)
        
        # Main weather panel (left)
        self.main_panel = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(height=100),
                    ft.Text("Search for a city", size=26, color="#6b7280", weight=ft.FontWeight.W_500, text_align=ft.TextAlign.CENTER),
                    ft.Text("Enter a city name above to see weather", size=14, color="#4b5563", text_align=ft.TextAlign.CENTER),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            bgcolor="#252540",
            border_radius=20,
            padding=25,
            expand=True,
        )
        
        # Forecast panel (right)
        self.forecast_panel = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("7-DAY FORECAST", size=13, color="#6b7280", weight=ft.FontWeight.BOLD),
                    ft.Divider(height=20, color="transparent"),
                    ft.Text("Search a city to see forecast", size=13, color="#4b5563"),
                ],
            ),
            bgcolor="#252540",
            border_radius=20,
            padding=25,
            width=280,
        )
        
        # Build page
        self.page.add(
            ft.Container(
                content=ft.Column(
                    controls=[
                        # Search row
                        ft.Row(
                            controls=[search_container, search_btn, self.loading],
                            spacing=10,
                        ),
                        # Error message
                        self.error_text,
                        # Spacer
                        ft.Container(height=15),
                        # Main content
                        ft.Row(
                            controls=[self.main_panel, self.forecast_panel],
                            spacing=20,
                            expand=True,
                            vertical_alignment=ft.CrossAxisAlignment.START,
                        ),
                    ],
                    spacing=8,
                    expand=True,
                ),
                bgcolor="#1a1a2e",
                padding=25,
                expand=True,
            )
        )
    
    def on_search(self, e):
        """Handle search."""
        self.page.run_task(self.fetch_weather)
    
    async def fetch_weather(self):
        """Fetch weather data."""
        city = self.city_input.value.strip() if self.city_input.value else ""
        
        if not city:
            self.error_text.value = "❌ Please enter a city name"
            self.error_text.visible = True
            self.page.update()
            return
        
        self.loading.visible = True
        self.error_text.visible = False
        self.page.update()
        
        try:
            weather = await self.weather_service.get_weather(city)
            forecast = await self.weather_service.get_forecast(city)
            
            self.current_weather_data = weather
            self.current_city = city
            self.add_to_history(city)
            
            self.update_display(weather, forecast)
            
        except WeatherServiceError as err:
            self.error_text.value = f"❌ {str(err)}"
            self.error_text.visible = True
        except Exception as err:
            import traceback
            print(f"ERROR: {traceback.format_exc()}")
            self.error_text.value = f"❌ Error: {str(err)}"
            self.error_text.visible = True
        finally:
            self.loading.visible = False
            self.page.update()
    
    def update_display(self, weather: dict, forecast: dict):
        """Update the weather display."""
        # Extract weather data
        city_name = weather.get("name", "Unknown")
        country = weather.get("sys", {}).get("country", "")
        temp = weather.get("main", {}).get("temp", 0)
        feels_like = weather.get("main", {}).get("feels_like", 0)
        description = weather.get("weather", [{}])[0].get("description", "").title()
        icon = weather.get("weather", [{}])[0].get("icon", "01d")
        wind = weather.get("wind", {}).get("speed", 0)
        humidity = weather.get("main", {}).get("humidity", 0)
        clouds = weather.get("clouds", {}).get("all", 0)
        
        # Hourly data
        hourly_list = forecast.get("list", [])[:6]
        hourly_cards = []
        for item in hourly_list:
            dt_txt = item.get("dt_txt", "")
            time_str = dt_txt.split(" ")[1][:5] if " " in dt_txt else "12:00"
            hr = int(time_str.split(":")[0])
            ampm = "AM" if hr < 12 else "PM"
            hr12 = hr if hr <= 12 else hr - 12
            if hr12 == 0: hr12 = 12
            
            hourly_cards.append(
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(f"{hr12}:00 {ampm}", size=12, color="#6b7280"),
                            ft.Image(src=f"https://openweathermap.org/img/wn/{item.get('weather', [{}])[0].get('icon', '01d')}@2x.png", width=45, height=45),
                            ft.Text(f"{item.get('main', {}).get('temp', 0):.0f}°", size=15, color="#ffffff", weight=ft.FontWeight.BOLD),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=2,
                    ),
                    padding=8,
                )
            )
        
        # Daily forecast
        daily_data = []
        seen = set()
        for item in forecast.get("list", []):
            date_str = item.get("dt_txt", "").split(" ")[0]
            if date_str and date_str not in seen:
                seen.add(date_str)
                dt = datetime.strptime(date_str, "%Y-%m-%d")
                daily_data.append({
                    "day": "Today" if len(daily_data) == 0 else dt.strftime("%a"),
                    "desc": item.get("weather", [{}])[0].get("main", "Clear"),
                    "icon": item.get("weather", [{}])[0].get("icon", "01d"),
                    "high": item.get("main", {}).get("temp_max", 0),
                    "low": item.get("main", {}).get("temp_min", 0),
                })
                if len(daily_data) >= 7:
                    break
        
        daily_rows = []
        for d in daily_data:
            daily_rows.append(
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text(d["day"], size=14, color="#9ca3af", width=50),
                            ft.Image(src=f"https://openweathermap.org/img/wn/{d['icon']}.png", width=28, height=28),
                            ft.Text(d["desc"], size=13, color="#6b7280", width=80),
                            ft.Container(expand=True),
                            ft.Text(f"{d['high']:.0f}", size=14, color="#ffffff", weight=ft.FontWeight.BOLD),
                            ft.Text(f"/{d['low']:.0f}", size=14, color="#6b7280"),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    border=ft.border.only(bottom=ft.BorderSide(1, "#2d2d4a")),
                    padding=ft.padding.symmetric(vertical=10),
                )
            )
        
        # Update main panel
        self.main_panel.content = ft.Column(
            controls=[
                # City + Icon row
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text(f"{city_name}, {country}", size=30, color="#ffffff", weight=ft.FontWeight.BOLD),
                                ft.Text(f"Chance of rain: {clouds}%", size=13, color="#9ca3af"),
                                ft.Container(height=5),
                                ft.Text(f"{temp:.0f}°", size=68, color="#ffffff", weight=ft.FontWeight.BOLD),
                            ],
                            spacing=2,
                        ),
                        ft.Container(expand=True),
                        ft.Image(src=f"https://openweathermap.org/img/wn/{icon}@4x.png", width=140, height=140),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),
                ft.Container(height=15),
                # Today's forecast
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("TODAY'S FORECAST", size=12, color="#6b7280", weight=ft.FontWeight.BOLD),
                            ft.Container(height=10),
                            ft.Row(controls=hourly_cards, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ],
                    ),
                    bgcolor="#1e1e38",
                    border_radius=15,
                    padding=20,
                ),
                ft.Container(height=15),
                # Air conditions
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Text("AIR CONDITIONS", size=12, color="#6b7280", weight=ft.FontWeight.BOLD),
                                    ft.Container(expand=True),
                                    ft.Container(
                                        content=ft.Text("See more", size=12, color="#ffffff"),
                                        bgcolor="#3b82f6",
                                        border_radius=20,
                                        padding=ft.padding.symmetric(horizontal=15, vertical=8),
                                    ),
                                ],
                            ),
                            ft.Container(height=15),
                            ft.Row(
                                controls=[
                                    self.condition_item(ft.Icons.THERMOSTAT, "Real Feel", f"{feels_like:.0f}°"),
                                    self.condition_item(ft.Icons.AIR, "Wind", f"{wind:.1f} km/h"),
                                ],
                            ),
                            ft.Container(height=10),
                            ft.Row(
                                controls=[
                                    self.condition_item(ft.Icons.WATER_DROP, "Humidity", f"{humidity}%"),
                                    self.condition_item(ft.Icons.WB_SUNNY, "UV Index", "3"),
                                ],
                            ),
                        ],
                    ),
                    bgcolor="#1e1e38",
                    border_radius=15,
                    padding=20,
                ),
            ],
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
        )
        
        # Update forecast panel
        self.forecast_panel.content = ft.Column(
            controls=[
                ft.Text("7-DAY FORECAST", size=13, color="#6b7280", weight=ft.FontWeight.BOLD),
                ft.Container(height=10),
                ft.Column(controls=daily_rows, spacing=0),
            ],
            scroll=ft.ScrollMode.AUTO,
        )
        
        self.page.update()
    
    def condition_item(self, icon, label, value):
        """Create condition item."""
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(icon, color="#6b7280", size=22),
                    ft.Column(
                        controls=[
                            ft.Text(label, size=12, color="#6b7280"),
                            ft.Text(value, size=18, color="#ffffff", weight=ft.FontWeight.BOLD),
                        ],
                        spacing=2,
                    ),
                ],
                spacing=12,
            ),
            expand=True,
        )


def main(page: ft.Page):
    """Main entry point."""
    WeatherApp(page)


if __name__ == "__main__":
    ft.app(target=main)