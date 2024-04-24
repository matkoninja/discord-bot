import discord
from discord.ext import commands

# Define intents
intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.message_content = True  # Allow bot to read message content



# Initialize the Bot with the specified intents
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

@bot.command()
async def setup_roles(ctx):
    roles = [
    "PV123 Základy vizuální komunikace",
    "PV078 Grafický design I",
    "VV035 3D Modeling",
    "PV066 Typografie I",
    "PV084 Písmo I",
    "PV067 Typography II",
    "PV083 Graphic Design II",
    "PV085 Type Design II",
    "PV257 Graphic Design and Multimedia Project",
    "PV259 Generative Design Programming",
    "PV268 Digital Design",
    "VV051 Animation",
    "VV036 3D Character Modeling",
    "PV156 Digital Photography",
    "VV067 Konceptuální a intermediální tvorba I",
    "VV050 Animace a vizualizace I",
    "PV101 Type Design III",
    "VV034 Fotografie - efekty při vzniku snímku",
    "VV045 Fotografie - portrétní fotografie",
    "VV042 Historické proměny fotografie",
    "VV033 Fotografie - práce se světlem a povrchy"
    ]  # Ensure all roles are unique

    categories = ["Gallery", "Courses"]
    roles.sort()
    category_objects = {}
    try:
        # Create categories first
        for category in categories:
            category_objects[category] = await ctx.guild.create_category(category)
            #await ctx.send(f"Category {category} created!")

        # Create roles and channels
        for role in roles:
            
            random_color = discord.Colour.random()
            new_role = await ctx.guild.create_role(name=role, color=random_color)

            #await ctx.send(f"Role {role} created!")

            for cat in categories:
                overwrites = {
                    ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    new_role: discord.PermissionOverwrite(read_messages=True)
                }
                channel = await ctx.guild.create_text_channel(name=f"{role}", category=category_objects[cat], overwrites=overwrites)
                #await ctx.send(f"Channel {channel.name} created in category {cat}!")
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

@bot.command()
async def update_gallery_permissions(ctx):
    # Fetch the category by name
    gallery_category = discord.utils.get(ctx.guild.categories, name="Gallery")
    if gallery_category is None:
        await ctx.send("Gallery category does not exist!")
        return
    
    # Define permission overwrite for everyone
    overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=True)
    }

    # Update permissions for each channel in the Gallery category
    for channel in gallery_category.channels:
        await channel.edit(overwrites=overwrites)
        await ctx.send(f"Updated permissions for {channel.name}")


@bot.command()
async def cleanup(ctx):
    # Optional: Clean up by deleting roles, channels, categories
    for category in ctx.guild.categories:
        continue
        for channel in category.channels:
            await channel.delete()
        await category.delete()
    for role in ctx.guild.roles:
        if role.name != "Admin" and role not in roles:
            try:
                await role.delete()
                await ctx.send(f"Deleted role: {role.name}")
            except discord.Forbidden:
                await ctx.send(f"Do not have permission to delete role: {role.name}")
            except discord.HTTPException as e:
                await ctx.send(f"Failed to delete role: {role.name}. Reason: {str(e)}")
# Important: Replace 'your_token_here' with your bot's actual token
bot.run('MTIzMjQyMDAzOTk0MTE2NTIyMA.G7l6A4._dAONLcVslyOFKJbYjivL1mgVUP-7tSS4VL2kA')
