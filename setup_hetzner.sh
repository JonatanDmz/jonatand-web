#!/bin/bash
# setup_hetzner.sh — Instala el blog daemon en el VPS Hetzner
# Ejecutar como root o con sudo en el VPS

set -e

echo "── Setup Blog Daemon · Negocios Inquietos ──"

# 1. Dependencias Python
pip install anthropic requests --break-system-packages

# 2. Clonar/actualizar el repo
if [ -d "/opt/jonatand-blog" ]; then
  echo "Repo ya existe, actualizando..."
  cd /opt/jonatand-blog && git pull
else
  echo "Clonando repo..."
  git clone https://github.com/jonatand-ia/jonatand-web.git /opt/jonatand-blog
fi

# 3. Configurar git en el VPS
cd /opt/jonatand-blog
git config user.email "jonatan@jonatand.com"
git config user.name "Jonatan Blog Daemon"

# 4. Crear directorio de logs
mkdir -p /opt/jonatand-blog/logs

# 5. Variables de entorno — editar con tus keys reales
cat > /opt/jonatand-blog/.env << 'EOF'
DART_TOKEN=tu_dart_token_aqui
ANTHROPIC_API_KEY=tu_anthropic_key_aqui
BLOG_REPO_PATH=/opt/jonatand-blog
EOF

echo ""
echo "⚠️  IMPORTANTE: Edita /opt/jonatand-blog/.env con tus keys reales"
echo "   nano /opt/jonatand-blog/.env"
echo ""

# 6. Script wrapper que carga el .env
cat > /opt/jonatand-blog/run_daemon.sh << 'EOF'
#!/bin/bash
set -a
source /opt/jonatand-blog/.env
set +a
cd /opt/jonatand-blog
python3 blog_daemon.py --once >> /opt/jonatand-blog/logs/daemon.log 2>&1
EOF
chmod +x /opt/jonatand-blog/run_daemon.sh

# 7. Cron — cada hora en punto
CRON_JOB="0 * * * * /opt/jonatand-blog/run_daemon.sh"
(crontab -l 2>/dev/null | grep -v "run_daemon"; echo "$CRON_JOB") | crontab -

echo ""
echo "✅ Setup completado"
echo ""
echo "Para probar manualmente una tarea:"
echo "  source /opt/jonatand-blog/.env"
echo "  python3 /opt/jonatand-blog/blog_daemon.py --task ID_DE_DART"
echo ""
echo "Para ver los logs:"
echo "  tail -f /opt/jonatand-blog/logs/daemon.log"
echo ""
echo "El cron corre cada hora. Para forzar ahora:"
echo "  /opt/jonatand-blog/run_daemon.sh"
