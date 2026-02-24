import discord
from discord.ext import commands
from discord import app_commands
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


# ===== VIEW DO BOTÃO =====
class PostView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🔗 Abrir Instagram", style=discord.ButtonStyle.link, url="https://instagram.com/")
    async def instagram_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass


# ===== COMANDO =====
@bot.command()
async def postar(ctx, titulo: str, descricao: str, imagem_url: str = None):
    embed = discord.Embed(
        title=titulo,
        description=descricao,
        color=discord.Color.purple()
    )

    embed.set_author(
        name=ctx.author.display_name,
        icon_url=ctx.author.display_avatar.url
    )

    if imagem_url:
        embed.set_image(url=imagem_url)
    else:
        embed.set_image(
            url="https://i.imgur.com/Exemplo.jpg"  # coloque uma imagem válida depois
        )

    view = PostView()
    await ctx.send(embed=embed, view=view)


# ===== EVENTO READY =====
@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")


# ===== RAILWAY TOKEN =====
if __name__ == "__main__":
    TOKEN = os.getenv("TOKEN")

    if not TOKEN:
        raise ValueError("TOKEN não encontrada nas variáveis de ambiente!")

    bot.run(TOKEN)