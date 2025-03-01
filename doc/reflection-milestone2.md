# Milestone 2 Reflection

## Premier League Dashboard

### Mohammed Bayati, Suneet D'Silva, Seamus Riordan-Short

Our dashboard allows for interactive visualization of 20 years of match data from the English Premier League. Users can filter the data with checkboxes to select only the teams and seasons they are interested in seeing. In a future version we hope to add a pop-up map (usually hidden) in this section that shows the locations of all selected teams. Another potential future feature might be "Select all" and "Select none" buttons or a different type of input here (such as sliders or entry fields) to make the team/season selection process quicker. Users can also choose between seeing data on match wins, or on goals scored. We hope to add more choices here later, as there are many additional match statistics available in the underlying data set.

We used Bootstrap for the layout of the dashboard page. Our layout is close to how we want it to look when viewed on a normal computer monitor, but right now the layout is broken on mobile screens or smaller windows. Well-designed Bootstrap should handle resizing, and we will work on improving this behaviour.

There are two pie charts that show the selected match statistic, one aggregated by teams and one aggregated by seasons. There are also two timelines on the bottom, with one showing the selected match stat aggregated per season, and the other showing it on a match-by-match basis. At this stage we have been focusing on performance and ensuring that data are called and displayed accurately; some of the visualizations (particularly the match-by-match timeline) are difficult to read and we will prioritize improving the display of these plots for future milestones.

We included a custom stylesheet that uses colour and font faces meant to emulate the official branding of the English Premier League. So far we have done minimal theming here, just changing the fonts used for text, its colour, and the style/colour of scrollbars in the checkboxes section. Now that the stylesheet is implemented we will tweak the theme in future milestones. We also made sure that in the pie charts and timelines, the colours used to represent selected teams accurately reflect those clubs' branding. If time permits we may update this so that each team has two colours associated with it, allowing for more distinctive theming for each team.
