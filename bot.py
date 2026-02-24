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
        self.likes = 0
        self.users_who_liked = set()
        self.thread = None  # guarda a thread criada

    # ===== BOTÃO CURTIR =====
    @discord.ui.button(label="❤️ 0", style=discord.ButtonStyle.secondary)
    async def like(self, interaction: discord.Interaction, button: discord.ui.Button):

        if interaction.user.id in self.users_who_liked:
            await interaction.response.send_message(
                "❌ Você já curtiu esse post!",
                ephemeral=True
            )
            return

        self.users_who_liked.add(interaction.user.id)
        self.likes += 1
        button.label = f"❤️ {self.likes}"

        await interaction.response.edit_message(view=self)

    # ===== BOTÃO COMENTAR =====
    @discord.ui.button(label="💬 Comentar", style=discord.ButtonStyle.primary)
    async def comment(self, interaction: discord.Interaction, button: discord.ui.Button):

        # Se já existe thread, só manda o usuário pra ela
        if self.thread:
            await interaction.response.send_message(
                f"💬 Comente aqui: {self.thread.mention}",
                ephemeral=True
            )
            return

        # Cria thread se ainda não existe
        self.thread = await interaction.message.create_thread(
            name="💬 Comentários"
        )

        await interaction.response.send_message(
            f"✅ Thread criada: {self.thread.mention}",
            ephemeral=True
        )


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
