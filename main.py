import init
import os
import discord
from discord.ext import commands
import asyncio
import nest_asyncio
import threading
from flask import Flask

nest_asyncio.apply()

# ====================================================================
# SERVIDOR WEB INTERNO PARA RENDER
# ====================================================================
app = Flask('')

@app.route('/')
def home():
    return "¡Bot de NicoShop en línea 24/7 en Render!"

def mantener_vivo():
    app.run(host='0.0.0.0', port=10000)

# ====================================================================
# CONFIGURACIÓN GENERAL - NICOSHOP
# ====================================================================
TOKEN_BOT = os.getenv("TOKEN_DISCORD")

ID_CANAL_REGLAS = 1549569523038822501       
ID_ROL_A_DAR = 1549569521566875752          
ID_CANAL_BIENVENIDAS = 1549569523038822502  

COLOR_ANUNCIO = 39423

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# ====================================================================
# LÓGICA DEL BOTÓN INTERACTIVO NATIVO DE REGLAS
# ====================================================================
class VistaVerificacionNativa(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="INICIAR", style=discord.ButtonStyle.green, emoji="✅", custom_id="boton_iniciar_sapphire")
    async def asignar_rol_directo(self, interaction: discord.Interaction, button: discord.ui.Button):
        rol = interaction.guild.get_role(ID_ROL_A_DAR)
        if not rol:
            return
        if rol in interaction.user.roles:
            await interaction.response.send_message("ℹ️ Tu cuenta ya tiene asignado este rol de acceso.", ephemeral=True)
        else:
            try:
                await interaction.user.add_roles(rol)
                await interaction.response.send_message("✅ ¡Rol asignado correctamente! Bienvenido a NicoShop.", ephemeral=True)
            except discord.Forbidden:
                await interaction.response.send_message("❌ Error de jerarquía: Sube el rol del Bot en la lista de Discord.", ephemeral=True)

@bot.event
async def on_member_join(member):
    canal = bot.get_channel(ID_CANAL_BIENVENIDAS)
    if not canal:
        print(f"❌ Error: No se encontró el canal de bienvenidas.")
        return

    texto_contenido = f"👾 Bienvenid@ {member.mention} a **{member.guild.name}**!👾"

    bienvenida_texto = (
        "Bienvenidos a la comunidad de Nicoshop\n\n"
        "Nos alegra tenerte con nosotros. Aquí encuentras los mejores precios en general 🥇\n\n"
        "<#1549569523038822501> Para comenzar dentro de la comunidad y entender las reglas.\n"
        "<#1549569523038822503> para estar al tanto de los anuncios e información. 📢"
    )

    embed = discord.Embed(description=bienvenida_texto, color=COLOR_ANUNCIO)

    try:
        await canal.send(content=texto_contenido, embed=embed)
        print(f"👋 ¡Bienvenida enviada con éxito a {member.name}!")
    except discord.Forbidden:
        print("❌ Error: El bot no tiene permisos para escribir en el canal de bienvenidas.")

@bot.event
async def on_ready():
    print(f"\n🟢 [SISTEMA MAESTRO ONLINE - NICOSHOP]")
    print(f"🤖 Bot conectado como: {bot.user}")
    print("👉 Celda activa. Vigilando reglas y bienvenidas al mismo tiempo.")
    
    canal = bot.get_channel(ID_CANAL_REGLAS)
    if canal:
        reglas_texto = (
            "🤝 **1. RESPETO ANTE TODO**\n\n"
            "• Trato Cordial: Trata a todos (staff, clientes y visitantes) con educación.\n"
            "• Cero Tolerancia: Prohibidos los insultos, el acoso, la discriminación o cualquier lenguaje ofensivo.\n"
            "• Diversión Sana: Las bromas son bienvenidas, siempre y cuando no dañen ni incomoden a otros.\n\n"
            "💎 **2. TRANSPARENCIA EN VENTAS Y COMPRAS**\n\n"
            "• Claridad Total: Precios, métodos de pago y formas de entrega deben ser públicos y claros en los canales correspondientes.\n"
            "• Canales Específicos: Las ofertas de UGC y Robux solo se permiten en las secciones habilitadas para ello.\n\n"
            "🚫 **3. PROHIBIDO ESTAFAR (ZERO TOLERANCE)**\n\n"
            "• Cualquier intento de engaño resultará en un baneo permanente inmediato y reporte masivo a otras comunidades de confianza. ¡Aquí jugamos limpio!\n\n"
            "📁 **4. USO DE CANALES CORRECTOS**\n\n"
            "• Cada canal tiene un propósito (ventas, soporte, dudas, presentaciones). Por favor, mantén el orden y no envíes mensajes fuera de lugar.\n"
            "• Sin Spam: No envíes mensajes repetitivos, cadenas ni publicidad de otros servidores sin autorización previa de un Admin.\n\n"
            "🔒 **5. PRIVACIDAD Y CONFIANZA**\n\n"
            "• Protection de Datos: No compartas información personal ajena (IP, direcciones, nombres reales).\n"
            "• Confidencialidad: Los detalles de las transacciones son privados entre el comprador, el vendedor y el Staff mediador.\n\n"
            "🛡️ **6. SOPORTE Y MODERACIÓN**\n\n"
            "• Si tienes un problema, contacta a los moderadores. No intentes hacer \"justicia por tu cuenta\" ni realices funas públicas dentro del servidor. Usa el sistema de tickets/soporte.\n\n"
            "⚠️ **7. REGLAS DE ROBLOX Y EDAD**\n\n"
            "• Roblox TOS: Todo intercambio debe cumplir estrictamente con los Términos de Servicio de Roblox.\n"
            "• Ambiente Familiar: Somos una comunidad apta para mayores de 13/16 años. Evita el lenguaje soez extremo y el contenido +18.\n\n"
            "Nico Shop, un lugar para aprender, comprar seguro y compartir nuestra pasión por Roblox.\n"
            "Al permanecer en el servidor, aceptas cumplir estas normas.\n\n"
            "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n"
            "#  𝐂𝐀𝐍𝐀𝐋𝐄𝐒 𝐄𝐍 𝐍𝐈𝐂𝐎𝐒𝐇𝐎𝐏"
            "\n\n<#1549569523038822503> Canal destinado a anuncios y comunicados importantes del servidor."
            "\n\n<#1549622368287334530> Espacio donde puedes encontrar nuestra comunidad de Roblox y disfrutar de nuestro catalogo de tienda."
            "\n\n<#1549646797767712879> Consulta aquí los precios y tarifas de nuestros productos o servicios."
            "\n\n<#1549647418025320468> Aquí encontrarás nuestras promociones y ofertas especiales."
            "\n\n<#1549650947280601108> Contenido limitado, exclusivo o disponible por tiempo limitado."
            "\n\n<#1549677334926336000> Canal destinado a sorteos, regalos y dinámicas especiales."
            "\n\n<#1549569523395330062> Chat principal para conversar, compartir ideas y pasar el rato."
            "\n\n<#1549569523395330064> ¿Tienes alguna duda? Déjala aquí y recibe ayuda de la comunidad."
            "\n\n<#1549569523395330066> Comparte y disfruta de contenido multimedia relacionado con la comunidad."
            "\n\n<#1549569523395330067> Espacio para compartir diseños, creaciones, dibujos y contenido artístico."
            "\n\n<#1549569523756044299> Canal de soporte para solicitar ayuda o resolver inconvenientes."
            "\n\n<#1549678588100485180> Canal de voz para escuchar música y disfrutarla junto a la comunidad."
            "\n\n<#1549679253748981780> Canal de voz para jugar, conversar y pasar un rato relajado."
            "\n\n<#1549679422737621093> Canal de voz destinado a realizar y participar en sorteos."
            "\n\n*A continuación encontrarás un botón de iniciar en la parte inferior donde debes clickear para aceptar que leíste las reglas y obtener tu rol para empezar!!*"
            "\n\n⬇️⬇️⬇️"
        )
        embed = discord.Embed(title="【📜】┃𝐑𝐄𝐆𝐋𝐀𝐒", description=reglas_texto, color=COLOR_ANUNCIO)
        await canal.send(embed=embed, view=VistaVerificacionNativa())
        print("✅ S1: Mensaje de reglas con botón verde republicado.")

async def main():
    # Iniciamos el servidor web Flask en segundo plano
    t = threading.Thread(target=mantener_vivo)
    t.daemon = True
    t.start()
    # Arrancamos el bot de Discord de forma segura
    try:
        await bot.start(TOKEN_BOT)
    except Exception as e:
        print(f"Error al iniciar el bot: {e}")

if __name__ == "__main__":
    asyncio.run(main())

