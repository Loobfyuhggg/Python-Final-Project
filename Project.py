# Importing necessary libraries
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

class SentimentAnalysisApp:

# TO DO: complete the __init__ function

    def __init__(self, data):
        if isinstance(data, dict):
            self.raw_data = pd.DataFrame(data)
        else:
            self.raw_data = data
        
        self.processed_data = self.raw_data.copy() # copy of raw data as a backup
        
        self.processed_data['cleaned_text'] = None
        self.processed_data['sentiment_polarity'] = None
        self.processed_data['sentiment_category'] = None
        self.daily_polarity = pd.DataFrame()
        self.daily_sentiment = pd.DataFrame()

   

# TO DO: define clean_data()

    def clean_data(self):
        # get rid of null rows
        self.processed_data.dropna(how= 'all', inplace = True)
        # gets rid of ones without text
        self.processed_data['text'] = self.processed_data['text'].replace('', pd.NA)
        self.processed_data.dropna(subset=['text'], inplace = True)

        # ensure date time format
        self.processed_data['date'] = pd.to_datetime(self.processed_data['date'], format='mixed')
        # gets rid of ones without a date
        self.processed_data.dropna(subset=['date'], inplace = True)

        # drops duplicates
        self.processed_data.drop_duplicates(inplace = True)



# TO DO: define clean_text()
    def clean_text(self):
        # gets rid of hashtags and @ symbols
        self.processed_data['cleaned_text'] = (
            self.processed_data['text']
            .astype(str)
            .str.replace("#", "", regex=False)
            .str.replace("@", "", regex=False)
        )



# TO DO: define get_sentiment()

    def get_sentiment(self):
        self.clean_data()
        self.clean_text()
        
        polarities = []
        
        # Loop through each index in the dataframe
        for idx in self.processed_data.index:
            # Get the text value and convert to string
            text_value = self.processed_data.loc[idx, 'cleaned_text']
            text_str = str(text_value) if not pd.isna(text_value) else ""
            
            if text_str.strip() == "":
                polarities.append(0)
                continue
            try:
                blob = TextBlob(text_str)
                polarities.append(blob.sentiment.polarity)
            except:
                polarities.append(0)
        
        # Assign the list to the dataframe column
        self.processed_data['sentiment_polarity'] = polarities
        return polarities


# TO DO: define analyze_sentiment()
    def analyze_sentiment(self):
        polarities = self.get_sentiment()
        polar_meter = []
        for i in polarities: #analyzes individual posts
            if i >= 0.07:
                polar_meter.append('Positive')
            elif i <= -0.07:
                polar_meter.append('Negative')
            else:
                polar_meter.append('Neutral')
        self.processed_data['sentiment_category'] = polar_meter

        self.daily_polarity = self.processed_data.groupby('date')['sentiment_polarity'].mean().reset_index()

        daily_categories = []
        for polarity in self.daily_polarity['sentiment_polarity']:
            if polarity >= 0.07:
                daily_categories.append('Positive')
            elif polarity <= -0.07:
                daily_categories.append('Negative')
            else:
                daily_categories.append('Neutral')
        
        self.daily_sentiment = pd.DataFrame({'date': self.daily_polarity['date'],'sentiment_category': daily_categories})
        
        
        


# TO DO: define plot_sentiment_trend()
    def plot_sentiment_trend(self):
        plt.figure(figsize=(12, 6))
        
        plt.scatter(
            self.processed_data['date'],
            self.processed_data['sentiment_polarity'],
            c=self.processed_data['sentiment_polarity'],
            cmap='coolwarm',  # Blue-Red colormap
            s=80,
            alpha=0.7,
            edgecolors='black',
            linewidth=1.5
        )
        
        plt.colorbar(label='Sentiment Polarity')
        plt.axhline(0, color='gray', linestyle='--', alpha=0.5)
        plt.title('Sentiment Distribution Over Time', fontweight='bold')
        plt.xlabel('Date')
        plt.ylabel('Sentiment Polarity')
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, alpha=0.3, axis='y')
        plt.ylim(-1.1, 1.1)
        plt.tight_layout()
        plt.show()





# TO DO: define print_sentiment_summary()
    def print_sentiment_summary(self):
        print(self.daily_sentiment)

        


# TO DO: define plot_sentiment_distribution()
    def plot_sentiment_distribution(self):
        daily_data = self.daily_polarity
        
        plt.figure(figsize=(12, 6))
        plt.plot(daily_data['date'], daily_data['sentiment_polarity'], 
                marker='o', linewidth=2, markersize=8)
        plt.title('Sentiment Trend Over Time')
        plt.xlabel('Date')
        plt.ylabel('Average Sentiment Score')
        plt.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
            



# Sample dataset for demo (Replace this with actual dataset if actual dataset is used)

file_path = r"C:\Users\gshar\OneDrive\Desktop\School Stuff\CS500Project\Untitled spreadsheet - twitter_dataset (1).csv" #Note, you'll have to change the file path to whatever the csv is! the csv should have a text column and date column
data = pd.read_csv(file_path)

# Create an instance of the SentimentAnalysisApp
app = SentimentAnalysisApp(data)



# Analyze sentiment

# TO DO: call app’s analyze_sentiment() 
app.analyze_sentiment()


# Print the dataframe to see the sentiment classification
print(app.processed_data)

# TO DO: call print to print data



# Plot sentiment trends over time

# TO DO: call app’s plot_sentiment_trend()
app.plot_sentiment_trend()


# Print sentiment summary

# TO DO: call app’s print_sentiment_summary()
app.print_sentiment_summary()


# Visualize sentiment distribution

# TO DO: call app’s plot_sentiment_distribution()

app.plot_sentiment_distribution()



