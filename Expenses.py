import asyncio
import os
from datetime import datetime, timedelta, timezone

import discord
import matplotlib.pyplot as plt
import pandas as pd
from redbot.core import commands

import io

# Matplotlib configuration
plt.switch_backend('agg')

class Expenses(commands.Cog):
    """Discord COG that tracks the expenses of multiple people in a specific channel"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def broke(self, ctx, person: discord.Member, time_range: str = "alltime"):
        """Shows the expenses of a person for various games."""
        
        # Collect data
        filtered_data = await self.collect_data(ctx.channel, person, time_range)

        if filtered_data:
            # Process data and create chart
            df = pd.DataFrame(filtered_data)
            game_expenses = df.groupby("Game")["Amount"].sum()

            # Create chart
            plt.figure(figsize=(10, 6))
            bar_plot = game_expenses.plot(kind="bar", width=0.3)
            self.format_plot(bar_plot, person.name, time_range)

            # Save the plot to a bytes buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)

            # Send the chart directly to the channel
            await self.send_chart(ctx, person, buf)
        
            # Close the plot to free up memory
            plt.close()
        else:
            await ctx.send(f"No matching expenses found for {person.mention}.")

    @commands.command()
    async def compare(self, ctx, time_range: str = "alltime"):
        """Compares the expenses among all people"""
        
        # Collect data
        try:
            filtered_data = await self.collect_data(ctx.channel, None, time_range)
        except:
            await self.send_error(ctx, "Error", "Parameter <days> must be a positive integer")
            return

        if filtered_data:
            # Process data and create chart
            df = pd.DataFrame(filtered_data)
            df["Amount"] = pd.to_numeric(df["Amount"])
            
            expenses_by_person = df.groupby("Author")["Amount"].sum()

            # Create chart
            plt.figure(figsize=(10, 6))
            bar_plot = expenses_by_person.plot(kind="bar", width=0.3)
            self.format_plot(bar_plot, "All expenses of all people", time_range)

            # Save the plot to a bytes buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)

            # Send the chart directly to the channel
            await self.send_chart(ctx, None, buf)
        
            # Close the plot to free up memory
            plt.close()
        else:
            await self.send_error(ctx, "Error", "No Expenses found")

    async def collect_data(self, channel, person, time_range):
        """Gets all data of a channel"""
        filtered_data = []
        time_ago = await self.get_time_ago(time_range)

        async for message in channel.history(limit=1000):
            if (not person or message.author == person) and message.created_at >= time_ago:
                content = message.content.strip()
                try:
                    if '€' in content:
                        amount_str, game = content.split('€', 1)
                        amount = float(amount_str.strip().replace(',', '.'))
                        game = game.strip().lower()
                        
                        filtered_data.append({
                            "Amount": amount,
                            "Game": game,
                            "Author": message.author.name
                        })
                except (ValueError, IndexError):
                    continue  # Skip invalid messages

        return filtered_data

    async def get_time_ago(self, time_range):
        """Calculates the requested time range"""
        if time_range == "alltime":
            return datetime(2022, 1, 1, tzinfo=timezone.utc)
        else:
            days = int(time_range)
            return datetime.now(timezone.utc) - timedelta(days=days)

    def format_plot(self, bar_plot, title, time_range):
        """Formats the data diagram"""
        plt.xlabel("")
        plt.ylabel("Amount in €", fontsize=25)
        plt.title(f"{title} ({'Total' if time_range == 'alltime' else time_range + ' Days'})", fontsize=25)
        plt.xticks(rotation=0, fontsize=20)
        plt.yticks(fontsize=15)

        for rect in bar_plot.patches:
            height = rect.get_height()
            plt.annotate(f"{height:.0f} €", 
                         xy=(rect.get_x() + rect.get_width() / 2, height),
                         xytext=(0, 3), 
                         textcoords="offset points", 
                         ha="center", va="bottom", fontsize=10)

    async def send_chart(self, ctx, person, chart):
        """Sends the message back to the discord channel and removes it after some time"""
        file = discord.File(chart, filename="chart.png")
        message = await ctx.send(f"Here are the expenses{' of ' + person.mention if person else ''}:", file=file)
        await ctx.message.delete()
        await asyncio.sleep(120)
        await message.delete()

    async def send_error(self, ctx, title, error):
        embed = discord.Embed(
            title=title,
            description="```" + error + "```",
            color=discord.Color.red()
        )
                
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Expenses(bot))