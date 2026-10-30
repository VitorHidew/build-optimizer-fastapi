const target = document.querySelector('#target');
const result = document.querySelector('#result');
const button = document.querySelector('#optimize');

async function loadCatalog() {
  const response = await fetch('/api/catalog');
  if (!response.ok) throw new Error('Não foi possível carregar o catálogo.');
  const catalog = await response.json();
  target.innerHTML = catalog.targets.map(item => `<option value="${item.id}">${item.name}</option>`).join('');
  result.textContent = 'Selecione um alvo e execute a otimização.';
}

async function optimize() {
  button.disabled = true;
  result.textContent = 'Calculando combinações...';
  try {
    const response = await fetch(`/api/optimize?target_id=${encodeURIComponent(target.value)}`);
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || 'Falha ao otimizar.');
    result.textContent = [
      `Arma: ${data.weapon}`,
      `Armaduras: ${data.armor.join(', ')}`,
      `Alvo: ${data.target}`,
      `Dano estimado: ${data.estimated_damage}`,
      `Defesa: ${data.total_defense}`,
      `Pontuação: ${data.score}`,
      '',
      ...data.explanation,
    ].join('\n');
  } catch (error) {
    result.textContent = error.message;
  } finally {
    button.disabled = false;
  }
}

button.addEventListener('click', optimize);
loadCatalog().catch(error => { result.textContent = error.message; });
