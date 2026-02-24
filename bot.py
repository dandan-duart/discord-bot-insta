import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


class PostView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.likes = 0
        self.users_who_liked = set()

    @discord.ui.button(label="❤️ 0", style=discord.ButtonStyle.secondary)
    async def like(self, interaction: discord.Interaction, button: discord.ui.Button):

        if interaction.user.id in self.users_who_liked:
            await interaction.response.send_message(
                "Você já curtiu esse post!",
                ephemeral=True
            )
            return

        self.users_who_liked.add(interaction.user.id)
        self.likes += 1
        button.label = f"❤️ {self.likes}"

        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="💬 Comentar", style=discord.ButtonStyle.primary)
    async def comment(self, interaction: discord.Interaction, button: discord.ui.Button):

        # Evita criar múltiplas threads
        if interaction.message.thread:
            await interaction.response.send_message(
                "Já existe uma thread de comentários!",
                ephemeral=True
            )
            return

        thread = await interaction.message.create_thread(
            name="💬 Comentários do post",
            auto_archive_duration=60
        )

        await interaction.response.send_message(
            f"Thread criada: {thread.mention}",
            ephemeral=True
        )


@bot.command()
async def post(ctx, *, imagem_url: str = None):
    """
    !post URL_DA_IMAGEM
    """

    embed = discord.Embed(
        description="📸 **Novo post!**",
        color=discord.Color.dark_gray()
    )

    embed.set_author(
        name=ctx.author.display_name,
        icon_url=ctx.author.display_avatar.url
    )

    if imagem_url:
        embed.set_image(url=imagem_url)
    else:
        embed.set_image(
            url="https://i.imgur.com/Exemplo.jpg"  # coloque uma imagem padrão válida
        )

    view = PostView()
    await ctx.send(embed=embed, view=view)


@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")


bot.run(TOKEN)