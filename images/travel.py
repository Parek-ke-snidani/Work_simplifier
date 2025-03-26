from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.properties import StringProperty, BooleanProperty, ListProperty, ObjectProperty
from kivy.clock import Clock
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, Rectangle
from kivy.uix.floatlayout import FloatLayout  # Added for floating button
from kivy.gesture import Gesture, GestureDatabase  # Added for swipe detection
import os
import sqlite3

# Initialize database
def init_database():
    # Database initialization code remains unchanged
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'travel_tracker.db')
    
    # Ensure the data directory exists
    data_dir = os.path.dirname(db_path)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # Connect to database (creates it if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create tables if they don't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS continents (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE,
        image_path TEXT,
        display_order INTEGER,
        visible INTEGER
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS countries (
        id INTEGER PRIMARY KEY,
        name TEXT,
        continent_id INTEGER,
        flag_path TEXT,
        visited INTEGER DEFAULT 0,
        FOREIGN KEY (continent_id) REFERENCES continents (id),
        UNIQUE (name, continent_id)
    )
    ''')
    
    # Dictionary with countries by continent
    countries_by_continent = {
        'Africa': ['Algeria', 'Angola', 'Benin', 'Botswana', 'Burkina Faso', 'Burundi', 'Cape Verde', 'Cameroon', 'Central African Republic', 'Chad', 'Comoros', 'Congo', 'Côte d\'Ivoire', 'Djibouti', 'DR Congo', 'Egypt', 'Equatorial Guinea', 'Eritrea', 'Eswatini', 'Ethiopia', 'Gabon', 'Gambia', 'Ghana', 'Guinea', 'Guinea-Bissau', 'Kenya', 'Lesotho', 'Liberia', 'Libya', 'Madagascar', 'Malawi', 'Mali', 'Mauritania', 'Mauritius', 'Morocco', 'Mozambique', 'Namibia', 'Niger', 'Nigeria', 'Rwanda', 'Sao Tome and Principe', 'Senegal', 'Seychelles', 'Sierra Leone', 'Somalia', 'South Africa', 'South Sudan', 'Sudan', 'Tanzania', 'Togo', 'Tunisia', 'Uganda', 'Zambia', 'Zimbabwe'],
        'Asia': ['Afghanistan', 'Armenia', 'Azerbaijan', 'Bahrain', 'Bangladesh', 'Bhutan', 'Brunei', 'Cambodia', 'China', 'Cyprus', 'Georgia', 'India', 'Indonesia', 'Iran', 'Iraq', 'Israel', 'Japan', 'Jordan', 'Kazakhstan', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Lebanon', 'Malaysia', 'Maldives', 'Mongolia', 'Myanmar', 'Nepal', 'North Korea', 'Oman', 'Pakistan', 'Palestine', 'Philippines', 'Qatar', 'Russia', 'Saudi Arabia', 'Singapore', 'South Korea', 'Sri Lanka', 'Syria', 'Taiwan', 'Tajikistan', 'Thailand', 'Timor-Leste', 'Turkey', 'Turkmenistan', 'United Arab Emirates', 'Uzbekistan', 'Vietnam', 'Yemen'],
        'Europe': ['Albania', 'Andorra', 'Austria', 'Belarus', 'Belgium', 'Bosnia and Herzegovina', 'Bulgaria', 'Croatia', 'Czechia', 'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary', 'Iceland', 'Ireland', 'Italy', 'Kosovo', 'Latvia', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Malta', 'Moldova', 'Monaco', 'Montenegro', 'Netherlands', 'North Macedonia', 'Norway', 'Poland', 'Portugal', 'Romania', 'San Marino', 'Serbia', 'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'Switzerland', 'Ukraine', 'United Kingdom', 'Vatican City'],
        'North America': ['Antigua and Barbuda', 'Bahamas', 'Barbados', 'Belize', 'Canada', 'Costa Rica', 'Cuba', 'Dominica', 'Dominican Republic', 'El Salvador', 'Grenada', 'Guatemala', 'Haiti', 'Honduras', 'Jamaica', 'Mexico', 'Nicaragua', 'Panama', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Trinidad and Tobago', 'United States'],
        'South America': ['Argentina', 'Bolivia', 'Brazil', 'Chile', 'Colombia', 'Ecuador', 'Guyana', 'Paraguay', 'Peru', 'Suriname', 'Uruguay', 'Venezuela'],
        'Antarctica': ['Antarctica'],
        'Australia/Oceania': ['Australia', 'Fiji', 'Kiribati', 'Marshall Islands', 'Micronesia', 'Nauru', 'New Zealand', 'Palau', 'Papua New Guinea', 'Samoa', 'Solomon Islands', 'Tonga', 'Tuvalu', 'Vanuatu']
    }
    
    # Check if continents table is empty
    cursor.execute("SELECT COUNT(*) FROM continents")
    if cursor.fetchone()[0] == 0:
        # Insert default continents
        for i, continent in enumerate(['Africa', 'Asia', 'Europe', 'North America', 'South America', 'Antarctica', 'Australia/Oceania']):
            image_path = f'images/{continent.lower().replace(" ", "_").replace("/", "_")}.png'
            cursor.execute(
                "INSERT INTO continents (name, image_path, display_order, visible) VALUES (?, ?, ?, ?)",
                (continent, image_path, i, 1)
            )
            
            # Get the continent ID
            cursor.execute("SELECT id FROM continents WHERE name = ?", (continent,))
            continent_id = cursor.fetchone()[0]
            
            # Insert countries for this continent
            for country in countries_by_continent[continent]:
                flag_path = f'images/flags/{country.lower().replace(" ", "_").replace("\'", "")}.png'
                cursor.execute(
                    "INSERT INTO countries (name, continent_id, flag_path, visited) VALUES (?, ?, ?, ?)",
                    (country, continent_id, flag_path, 0)
                )
    
    conn.commit()
    conn.close()

# Initialize database on app start
init_database()

# Create gesture database for swipe detection
gesture_database = GestureDatabase()

# Create right to left swipe gesture
def right_to_left_line(points):
    g = Gesture()
    g.add_stroke(points)
    g.normalize()
    return g

def left_to_right_line(points):
    g = Gesture()
    g.add_stroke(points)
    g.normalize()
    return g

# Add swipe gestures to database
right_to_left_swipe = right_to_left_line([(0.0, 0.5), (1.0, 0.5)])
gesture_database.add_gesture(right_to_left_swipe)

left_to_right_swipe = left_to_right_line([(1.0, 0.5), (0.0, 0.5)])
gesture_database.add_gesture(left_to_right_swipe)

class SwipeDetector:
    def __init__(self, callback):
        self.touch_down_x = 0
        self.touch_down_y = 0
        self.callback = callback
        
    def on_touch_down(self, touch):
        self.touch_down_x = touch.x
        self.touch_down_y = touch.y
        return False
    
    def on_touch_up(self, touch):
        # Calculate swipe distance
        distance_x = touch.x - self.touch_down_x
        
        # If horizontal swipe distance is significant
        if abs(distance_x) > dp(100):
            # Left to right swipe (for back button)
            if distance_x > 0:
                self.callback()
                return True
        return False

class CountryButton(ButtonBehavior, BoxLayout):
    country_name = StringProperty('')
    country_id = StringProperty('')
    visited = BooleanProperty(False)
    flag_path = StringProperty('')
    
    def __init__(self, **kwargs):
        super(CountryButton, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(150)
        self.padding = dp(5)
        
        # Create flag image
        self.flag_image = Image(
            source=self.flag_path,
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(1, 0.8)
        )
        
        # Apply grayscale effect if not visited
        if not self.visited:
            self.flag_image.color = [0.5, 0.5, 0.5, 1]
        
        # Create country name label with improved text alignment
        self.country_label = Label(
            text=self.country_name,
            size_hint=(1, 0.2),
            color=(0, 0, 40, 1),
            font_size=dp(14),
            halign='center',
            valign='top'
        )
        self.country_label.bind(size=self.country_label.setter('text_size'))
        
        # Add widgets to layout
        self.add_widget(self.flag_image)
        self.add_widget(self.country_label)
    
    def on_release(self):
        # Toggle visited status
        self.visited = not self.visited
        
        # Update UI
        if self.visited:
            self.flag_image.color = [1, 1, 1, 1]  # Full color
        else:
            self.flag_image.color = [0.5, 0.5, 0.5, 1]  # Grayscale
        
        # Update database
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'travel_tracker.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE countries SET visited = ? WHERE id = ?",
            (1 if self.visited else 0, self.country_id)
        )
        
        conn.commit()
        conn.close()

class ContinentButton(ButtonBehavior, BoxLayout):
    continent_name = StringProperty('')
    continent_id = StringProperty('')
    image_source = StringProperty('')
    
    def __init__(self, **kwargs):
        super(ContinentButton, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(200)
        self.padding = dp(10)
        
        # Create continent image
        self.continent_image = Image(
            source=self.image_source,
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(1, 0.8)
        )
        
        # Create continent name label with improved text alignment
        self.continent_label = Label(
            text=self.continent_name,
            size_hint=(1, 0.2),
            color=(0, 0, 40, 1),
            font_size=dp(18),
            bold=True,
            halign='center', 
            valign='top'
        )
        self.continent_label.bind(size=self.continent_label.setter('text_size'))
        
        # Add widgets to layout
        self.add_widget(self.continent_image)
        self.add_widget(self.continent_label)
    
    def on_release(self):
        app = App.get_running_app()
        app.show_continent_countries(self.continent_name, self.continent_id)

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # Create header
        header = BoxLayout(size_hint_y=0.1)
        title = Label(text='Travel Tracker', font_size=dp(24), bold=True, color=(0, 0, 40, 1), size_hint_x=0.7)
        
        # Create buttons
        options_btn = Button(text='Options', size_hint_x=0.15)
        options_btn.bind(on_release=self.show_options)
        
        stats_btn = Button(text='Statistics', size_hint_x=0.15)
        stats_btn.bind(on_release=self.show_statistics)
        
        header.add_widget(title)
        header.add_widget(options_btn)
        header.add_widget(stats_btn)
        
        self.layout.add_widget(header)
        
        # Create scrollable content area for continents
        self.scroll_view = ScrollView()
        self.continents_layout = GridLayout(cols=2, spacing=dp(10), size_hint_y=None)
        self.continents_layout.bind(minimum_height=self.continents_layout.setter('height'))
        
        self.scroll_view.add_widget(self.continents_layout)
        self.layout.add_widget(self.scroll_view)
        
        self.add_widget(self.layout)
        
        # Schedule the update after the widget is added to the window
        Clock.schedule_once(self.update_continents_list)
    
    def on_enter(self):
        # Update continents list when returning to this screen
        self.update_continents_list()
    
    def update_continents_list(self, dt=None):
        self.continents_layout.clear_widgets()
        
        # Get continents from database
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'travel_tracker.db')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # This allows accessing columns by name
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT id, name, image_path FROM continents WHERE visible = 1 ORDER BY display_order"
        )
        
        continents = cursor.fetchall()
        conn.close()
        
        # Add continent buttons to the layout
        for continent in continents:
            btn = ContinentButton(
                continent_name=continent['name'],
                continent_id=str(continent['id']),
                image_source=continent['image_path']
            )
            self.continents_layout.add_widget(btn)
    
    def show_options(self, instance):
        app = App.get_running_app()
        app.root.current = 'options'
    
    def show_statistics(self, instance):
        app = App.get_running_app()
        app.root.current = 'statistics'

class ContinentScreen(Screen):
    continent_name = StringProperty('')
    continent_id = StringProperty('')
    
    def __init__(self, **kwargs):
        super(ContinentScreen, self).__init__(**kwargs)
        # Use FloatLayout as the main container to allow absolute positioning
        self.layout = FloatLayout()
        
        # Create a BoxLayout for the main content
        self.content_layout = BoxLayout(orientation='vertical', 
                                       padding=dp(10), 
                                       spacing=dp(10),
                                       size_hint=(1, 1))
        
        # Create header without back button
        header = BoxLayout(size_hint_y=0.1)
        
        self.title_label = Label(
            text='',
            font_size=dp(20),
            bold=True,
            color=(0, 0, 0, 1),
            size_hint_x=1
        )
        
        header.add_widget(self.title_label)
        
        self.content_layout.add_widget(header)
        
        # Create scrollable content area for countries
        self.scroll_view = ScrollView()
        self.countries_layout = GridLayout(cols=3, spacing=dp(10), size_hint_y=None)
        self.countries_layout.bind(minimum_height=self.countries_layout.setter('height'))
        
        self.scroll_view.add_widget(self.countries_layout)
        self.content_layout.add_widget(self.scroll_view)
        
        # Add the content layout to the main layout
        self.layout.add_widget(self.content_layout)
        
        # Create back button in lower right corner
        self.back_btn = Button(
            text='Back',
            size_hint=(0.2, 0.08),
            pos_hint={'right': 0.98, 'bottom': 0.02}  # Position in lower right corner
        )
        self.back_btn.bind(on_release=self.go_back)
        
        # Add back button to the layout
        self.layout.add_widget(self.back_btn)
        
        # Add swipe detection
        self.swipe_detector = SwipeDetector(self.go_back)
        
        self.add_widget(self.layout)
    
    def on_pre_enter(self):
        self.title_label.text = self.continent_name
        self.update_countries_list()
    
    def update_countries_list(self):
        self.countries_layout.clear_widgets()
        
        # Get countries from database
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'travel_tracker.db')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # This allows accessing columns by name
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT id, name, flag_path, visited FROM countries WHERE continent_id = ? ORDER BY name",
            (self.continent_id,)
        )
        
        countries = cursor.fetchall()
        conn.close()
        
        # Add country buttons to the layout
        for country in countries:
            btn = CountryButton(
                country_name=country['name'],
                country_id=str(country['id']),
                visited=bool(country['visited']),
                flag_path=country['flag_path']
            )
            self.countries_layout.add_widget(btn)
    
    def go_back(self, instance=None):
        app = App.get_running_app()
        app.root.current = 'main'
    
    def on_touch_down(self, touch):
        self.swipe_detector.on_touch_down(touch)
        return super(ContinentScreen, self).on_touch_down(touch)
    
    def on_touch_up(self, touch):
        if self.swipe_detector.on_touch_up(touch):
            return True
        return super(ContinentScreen, self).on_touch_up(touch)

class OptionsScreen(Screen):
    def __init__(self, **kwargs):
        super(OptionsScreen, self).__init__(**kwargs)
        # Use FloatLayout as the main container
        self.layout = FloatLayout()
        
        # Create a BoxLayout for the main content
        self.content_layout = BoxLayout(orientation='vertical',
                                       padding=dp(10),
                                       spacing=dp(10),
                                       size_hint=(1, 1))
        
        # Create header without back button
        header = BoxLayout(size_hint_y=0.1)
        
        title = Label(
            text='Options',
            font_size=dp(20),
            bold=True,
            color=(0, 0, 40, 1),
            size_hint_x=1
        )
        
        header.add_widget(title)
        
        self.content_layout.add_widget(header)
        
        # Create scrollable content area
        self.scroll_view = ScrollView()
        self.content = GridLayout(cols=1, spacing=dp(10), size_hint_y=None)
        self.content.bind(minimum_height=self.content.setter('height'))
        
        self.scroll_view.add_widget(self.content)
        self.content_layout.add_widget(self.scroll_view)
        
        # Add save button
        save_btn = Button(text='Save Changes', size_hint=(0.2, 0.08), pos_hint={'left': 0.98, 'bottom': 0.02})
        save_btn.bind(on_release=self.save_changes)
        self.content_layout.add_widget(save_btn)
        
        # Add the content layout to the main layout
        self.layout.add_widget(self.content_layout)
        
        # Create back button in lower right corner
        self.back_btn = Button(
            text='Back',
            size_hint=(0.2, 0.08),
            pos_hint={'right': 0.98, 'bottom': 0.02}  # Position in lower right corner
        )
        self.back_btn.bind(on_release=self.go_back)
        
        # Add back button to the layout
        self.layout.add_widget(self.back_btn)
        
        # Add swipe detection
        self.swipe_detector = SwipeDetector(self.go_back)
        
        self.add_widget(self.layout)
        
        # Initialize continent options dictionary
        self.continent_options = {}
    
    def on_pre_enter(self):
        self.load_options()
    
    def load_options(self):
        self.content.clear_widgets()
        self.continent_options = {}
        
        # Get continents from database
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'travel_tracker.db')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # This allows accessing columns by name
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT id, name, display_order, visible FROM continents ORDER BY display_order"
        )
        
        continents = cursor.fetchall()
        
        # Get total number of continents for order spinner
        total_continents = len(continents)
        conn.close()
        
        # Create options for each continent
        for continent in continents:
            continent_layout = BoxLayout(size_hint_y=None, height=dp(50))
            
            # Continent name label with vertical alignment
            label = Label(
                text=continent['name'], 
                size_hint_x=0.5, 
                color=(0, 40, 0, 1), 
                halign='left',
                valign='middle'
            )
            label.bind(size=label.setter('text_size'))
            
            # Visibility button
            visible_btn = Button(
                text='Visible' if continent['visible'] else 'Hidden',
                size_hint_x=0.25
            )
            visible_btn.continent_id = continent['id']
            visible_btn.is_visible = bool(continent['visible'])
            visible_btn.bind(on_release=self.toggle_visibility)
            
            # Order spinner
            order_spinner = Spinner(
                text=str(continent['display_order'] + 1),
                values=[str(i) for i in range(1, total_continents + 1)],
                size_hint_x=0.25
            )
            order_spinner.continent_id = continent['id']
            order_spinner.original_order = continent['display_order']
            order_spinner.bind(text=self.prepare_order_change)
            
            continent_layout.add_widget(label)
            continent_layout.add_widget(visible_btn)
            continent_layout.add_widget(order_spinner)
            
            self.content.add_widget(continent_layout)
            
            self.continent_options[continent['id']] = {
                'visible_btn': visible_btn,
                'order_spinner': order_spinner,
                'new_visibility': bool(continent['visible']),
                'new_order': continent['display_order']
            }
    
    def toggle_visibility(self, instance):
        instance.is_visible = not instance.is_visible
        instance.text = 'Visible' if instance.is_visible else 'Hidden'
        
        # Store the new visibility setting
        self.continent_options[instance.continent_id]['new_visibility'] = instance.is_visible
    
    def prepare_order_change(self, instance, value):
        new_order = int(value) - 1
        
        # Store the new order
        self.continent_options[instance.continent_id]['new_order'] = new_order
    
    def save_changes(self, instance):
        # Get database connection
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'travel_tracker.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Apply changes for each continent
        for continent_id, options in self.continent_options.items():
            cursor.execute(
                "UPDATE continents SET display_order = ?, visible = ? WHERE id = ?",
                (options['new_order'], 1 if options['new_visibility'] else 0, continent_id)
            )
        
        conn.commit()
        conn.close()
        
        # Show message
        instance.text = 'Changes Saved!'
        Clock.schedule_once(lambda dt: setattr(instance, 'text', 'Save Changes'), 2)
    
    def go_back(self, instance=None):
        app = App.get_running_app()
        app.root.current = 'main'
    
    def on_touch_down(self, touch):
        self.swipe_detector.on_touch_down(touch)
        return super(OptionsScreen, self).on_touch_down(touch)
    
    def on_touch_up(self, touch):
        if self.swipe_detector.on_touch_up(touch):
            return True
        return super(OptionsScreen, self).on_touch_up(touch)

class StatisticsScreen(Screen):
    def __init__(self, **kwargs):
        super(StatisticsScreen, self).__init__(**kwargs)
        # Use FloatLayout as the main container
        self.layout = FloatLayout()
        
        # Create a BoxLayout for the main content
        self.content_layout = BoxLayout(orientation='vertical',
                                       padding=dp(10),
                                       spacing=dp(10),
                                       size_hint=(1, 1))
        
        # Create header without back button
        header = BoxLayout(size_hint_y=0.1)
        
        title = Label(
            text='Statistics',
            font_size=dp(20),
            bold=True,
            color=(0, 0, 40, 1),
            size_hint_x=1
        )
        
        header.add_widget(title)
        
        self.content_layout.add_widget(header)
        
        # Create scrollable content area
        self.scroll_view = ScrollView()
        self.stats_layout = GridLayout(cols=1, spacing=dp(10), size_hint_y=None)
        self.stats_layout.bind(minimum_height=self.stats_layout.setter('height'))
        
        self.scroll_view.add_widget(self.stats_layout)
        self.content_layout.add_widget(self.scroll_view)
        
        # Add the content layout to the main layout
        self.layout.add_widget(self.content_layout)
        
        # Create back button in lower right corner
        self.back_btn = Button(
            text='Back',
            size_hint=(0.2, 0.08),
            pos_hint={'right': 0.98, 'bottom': 0.02}  # Position in lower right corner
        )
        self.back_btn.bind(on_release=self.go_back)
        
        # Add back button to the layout
        self.layout.add_widget(self.back_btn)
        
        # Add swipe detection
        self.swipe_detector = SwipeDetector(self.go_back)
        
        self.add_widget(self.layout)
    
    def on_pre_enter(self):
        self.update_statistics()
    
    def update_statistics(self):
        self.stats_layout.clear_widgets()
        
        # Get statistics from database
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'travel_tracker.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get total countries visited
        cursor.execute("SELECT COUNT(*) FROM countries WHERE visited = 1")
        total_visited = cursor.fetchone()[0]
        
        # Get total countries
        cursor.execute("SELECT COUNT(*) FROM countries")
        total_countries = cursor.fetchone()[0]
        
        # Display total statistics
        total_label = Label(
            text=f'Total Countries Visited: {total_visited}/{total_countries} ({total_visited/total_countries*100:.1f}%)',
            font_size=dp(18),
            color=(40, 0, 0, 1),
            size_hint_y=None,
            height=dp(40)
        )
        self.stats_layout.add_widget(total_label)
        
        # Get statistics for each continent
        cursor.execute("""
            SELECT c.name, 
                   SUM(CASE WHEN co.visited = 1 THEN 1 ELSE 0 END) as visited,
                   COUNT(co.id) as total
            FROM continents c
            JOIN countries co ON c.id = co.continent_id
            GROUP BY c.name
            ORDER BY c.display_order
        """)
        
        continent_stats = cursor.fetchall()
        conn.close()
        
        # Display statistics for each continent
        for continent_name, visited, total in continent_stats:
            percentage = (visited / total * 100) if total > 0 else 0
            continent_label = Label(
                text=f'{continent_name}: {visited}/{total} ({percentage:.1f}%)',
                font_size=dp(16),
                color=(0, 40, 0, 1),
                size_hint_y=None,
                height=dp(30)
            )
            self.stats_layout.add_widget(continent_label)
    
    def go_back(self, instance=None):
        app = App.get_running_app()
        app.root.current = 'main'
class TravelTrackerApp(App):
    def build(self):
        # Set up window for desktop
        Window.size = (dp(800), dp(600))
        Window.minimum_width = dp(400)
        Window.minimum_height = dp(400)
        
        # Create screen manager
        sm = ScreenManager()
        
        # Add screens
        main_screen = MainScreen(name='main')
        sm.add_widget(main_screen)
        
        continent_screen = ContinentScreen(name='continent')
        sm.add_widget(continent_screen)
        
        options_screen = OptionsScreen(name='options')
        sm.add_widget(options_screen)
        
        statistics_screen = StatisticsScreen(name='statistics')
        sm.add_widget(statistics_screen)
        
        # Set initial screen
        sm.current = 'main'
        
        return sm
    
    def show_continent_countries(self, continent_name, continent_id):
        continent_screen = self.root.get_screen('continent')
        continent_screen.continent_name = continent_name
        continent_screen.continent_id = continent_id
        self.root.current = 'continent'

if __name__ == '__main__':
    TravelTrackerApp().run()