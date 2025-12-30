Branch protection — recomendaciones para `main`

Sugerencia de configuración (recomendado):

1) Requerir status checks que pasen antes de merge
   - Check: `Run tests` (workflow: `.github/workflows/pytest.yml`)
   - Activar "Require branches to be up to date before merging" (strict)

2) Requerir revisiones antes del merge
   - "Require pull request reviews before merging"
   - `Required approving reviews` = 1 (o más, según equipo)
   - Opcional: habilitar "Dismiss stale pull request approvals when new commits are pushed"

3) Administradores
   - Recomiendo **no** deshabilitar la protección para administradores, dejar "Enforce for administrators" activado.

4) Pasos para aplicar (usando GitHub UI)
   - Repo → Settings → Branches → Add rule
   - Branch name pattern: `main`
   - Marcar: Require status checks to pass
   - Seleccionar: **Run tests**
   - Marcar: Require pull request reviews before merging
   - Opcional: Require conversation resolution

5) Aplicar usando la API / `gh` (ejemplo)

- Con GitHub CLI (`gh`) autenticado:

```bash
gh api --method PUT \
  -H "Accept: application/vnd.github+json" \
  /repos/:owner/:repo/branches/main/protection \
  -f required_status_checks='{"strict":true,"contexts":["Run tests"]}' \
  -f enforce_admins=true \
  -f required_pull_request_reviews='{"required_approving_review_count":1}'
```

- Con `curl` + token (set `GITHUB_TOKEN` o `TOKEN` en tu sesión):

```bash
curl -X PUT -H "Accept: application/vnd.github+json" \
     -H "Authorization: token $TOKEN" \
     https://api.github.com/repos/:owner/:repo/branches/main/protection \
     -d '{
       "required_status_checks": {"strict": true, "contexts": ["Run tests"]},
       "enforce_admins": true,
       "required_pull_request_reviews": {"required_approving_review_count": 1}
     }'
```


6) Notas
   - Revisa en la UI qué nombre exacto tiene el check (a veces aparece con el prefijo del workflow). En este repo el check es `Run tests`.
   - Después de aplicar, cualquier push directo a `main` que no provenga de un PR puede bloquearse según la configuración.

Si querés, puedo abrir un Pull Request con este archivo en `main` (hecho ya) y luego te paso las instrucciones para aplicar la regla (requiere privilegios de administrador en el repo). También puedo preparar el `gh`/`curl` comando con los valores del repo para que lo pegues y lo ejecutes tú mismo.  