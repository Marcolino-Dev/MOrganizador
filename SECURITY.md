# Política de Segurança

## Versões Suportadas

Atualmente, fornecemos atualizações de segurança para as seguintes versões:

| Versão | Suportada |
|--------|-----------|
| 1.0.x  | ✅ Sim    |
| < 1.0  | ❌ Não    |

## Reportando uma Vulnerabilidade

**Por favor, NÃO abra uma issue pública para vulnerabilidades de segurança.**

Em vez disso, reporte privadamente através de:

1. **GitHub Security Advisories** (preferido): Use a aba "Security" > "Report a vulnerability" neste repositório
2. **Email**: security@lairm.dev (se configurado)

### O que incluir no relatório

- Descrição da vulnerabilidade
- Passos para reproduzir (Proof of Concept)
- Impacto potencial
- Versão afetada
- Sugestão de correção (se tiver)

### Tempo de Resposta

- **Confirmação de recebimento**: ≤ 48 horas
- **Avaliação inicial**: ≤ 7 dias
- **Correção e release**: ≤ 30 dias (dependendo da severidade)

## Medidas de Segurança Implementadas

### Path Traversal Protection
- Validação rigorosa de caminhos (`_caminho_seguro`) em todas as operações de arquivo
- Resolução de caminhos absolutos antes de operações
- Verificação de que destino está dentro da pasta base

### Input Validation
- Sanitização de nomes de arquivo (`_sanitizar_nome`)
- Validação de nomes reservados do Windows (CON, PRN, AUX, NUL, COM1-9, LPT1-9)
- Rejeição de caracteres perigosos (`..`, `~`, `$`, `` ` ``, `|`, `;`, `&`, `<`, `>`)

### Symlink Protection
- Verificação `is_symlink()` antes de mover/processar arquivos
- Prevenção de link attacks

### Safe History Storage
- Histórico salvo em diretório de dados do usuário (`LOCALAPPDATA`/`XDG_DATA_HOME`)
- Não na pasta de trabalho (evita exposição acidental)
- Arquivo JSON com validação ao carregar

### Permission Handling
- Verificação de permissão de leitura/escrita antes de operar
- Tratamento gracioso de `PermissionError`
- Execução como usuário normal (não requer Admin)

## Boas Práticas para Usuários

1. **Execute como usuário normal** - não precisa de Administrador
2. **Feche arquivos abertos** - evita erros de permissão
3. **Verifique executáveis** - SmartScreen pode avisar (não assinado digitalmente)
4. **Mantenha atualizado** - use a versão mais recente para correções de segurança
5. **Backup importante** - sempre faça backup antes de organizar pastas críticas

## Histórico de Vulnerabilidades

| Data | Versão | CVE | Descrição | Severidade |
|------|--------|-----|-----------|------------|
| -    | -      | -   | Nenhuma vulnerabilidade conhecida | - |

## Hall of Fame / Agradecimentos

Agradecemos a pesquisadores que reportam vulnerabilidades responsavelmente:

- *(nenhum ainda - seja o primeiro!)*

---

**Última atualização**: 2026-11-16