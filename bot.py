import discord
from discord import app_commands
from discord.ext import commands

TOKEN = "TON_TOKEN_ICI"
ROLE_ID = 123456789012345678  # Remplace par l’ID du rôle à donner

intents = discord.Intents.default()
intents.guilds = True
intents.members = True  # Nécessaire pour donner un rôle

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree


@bot.event
async def on_ready():
    await tree.sync()
    print(f"✅ Connecté en tant que {bot.user}")


@tree.command(name="bingo", description="Vérifie ton code PIN secret")
@app_commands.describe(nombre="Entre ton numéro")
async def bingo(interaction: discord.Interaction, nombre: int):
    try:
        resultat = int((nombre + 6845321) / 2)
        resultat_str = f"{resultat:08d}"  # S'assure d’avoir au moins 8 chiffres

        A = int(resultat_str[-3:])          # les 3 derniers
        B = int(resultat_str[-6:-3])        # les 3 du milieu
        C = int(resultat_str[:2])           # les 2 premiers

        if (A + B) == C:
            # Donner le rôle
            role = interaction.guild.get_role(ROLE_ID)
            if role:
                await interaction.user.add_roles(role)
                await interaction.response.send_message("✅ PIN correct ! Rôle attribué.")
            else:
                await interaction.response.send_message("✅ PIN correct, mais le rôle est introuvable.")
        else:
            await interaction.response.send_message("❌ Ceci est un PIN incorrect.")

    except Exception as e:
        await interaction.response.send_message(f"Erreur : {str(e)}")


bot.run(TOKEN)
