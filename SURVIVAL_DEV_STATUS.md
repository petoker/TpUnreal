# 🧟 Project Status: Survival Horror RE4 Style (UADE - DAV)

## 📌 Contexto del Proyecto
- **Materia**: Desarrollo Avanzado de Videojuegos (UADE).
- **Género**: Survival Horror en tercera persona (cámara al hombro estilo *Resident Evil 4*).
- **Motor**: Unreal Engine 5.3 (Proyecto `TpUnreal`).
- **Condición clave de entrega**: 
  - Prohibido reutilizar/copiar de las carpetas de templates de Unreal.
  - Toda la arquitectura debe ser propia, modular y con nomenclatura estándar (`BP_`, `GM_`, `IA_`, `IMC_`, etc.).
  - Uso estricto del Gameplay Framework (`GameMode`, `PlayerController`, `Character`).
  - Uso de Enhanced Input, Behaviour Tree para IA, State Machine para animaciones y UMG para HUD.
  - Al menos 2 niveles jugables con progresión, zona segura inicial, menú principal, pausa y victoria/derrota.
  - Mínimo 2 interactuables en el mundo.

---

## 🛠️ Lo que ya está implementado (Content/SurvivalHorror/)

1. **Estructura de Carpetas**:
   - `Content/SurvivalHorror/Blueprints/Core`
   - `Content/SurvivalHorror/Blueprints/Characters`
   - `Content/SurvivalHorror/Blueprints/Interfaces`
   - `Content/SurvivalHorror/Blueprints/Items`
   - `Content/SurvivalHorror/Input/Actions`
   - `Content/SurvivalHorror/AI`
   - `Content/SurvivalHorror/UI`
   - `Content/SurvivalHorror/Maps`

2. **Enhanced Input**:
   - `IA_Move` (Axis2D)
   - `IA_Look` (Axis2D)
   - `IA_Aim` (Digital bool)
   - `IA_Shoot` (Digital bool)
   - `IA_Interact` (Digital bool)
   - `IMC_Survival` (Mapeo completo de WASD, Mouse XY, RMB, LMB, E).

3. **Gameplay Framework**:
   - `GM_SurvivalGameMode`: asignado como GameMode Override, tiene seteado el `DefaultPawnClass = BP_SurvivalCharacter` y `PlayerControllerClass = GM_SurvivalPlayerControlle`.
   - `GM_SurvivalPlayerControlle`: controlador base.

4. **Personaje (`BP_SurvivalCharacter`)**:
   - Malla asignada (`SKM_Manny` / `SKM_Quinn`).
   - `CameraBoom` configurado estilo RE4:
     - Target Arm Length = 220
     - Socket Offset = X: 0, Y: 45, Z: 25
     - Camera Lag habilitado (Speed: 12.0)
     - Use Pawn Control Rotation = True
   - `FollowCamera` hijo de `CameraBoom`.
   - Event Graph:
     - `IA_Look`: conecta a `Add Controller Yaw Input` (X) y `Add Controller Pitch Input` (Y).
     - `IA_Move`: conectado con `Get Control Rotation` (Target is Pawn) ➔ `Make Rotator (Yaw)` ➔ `Get Forward Vector` (Y) y `Get Right Vector` (X).
     - `IA_Aim`: sistema de apuntado con `TL_Aim` (Timeline Float 0 a 1 en 0.2s), `Lerp (Float)` para `Field Of View` (de 90 a 65), `bIsAiming`, `bUseControllerRotationYaw` y velocidad a 200/500 con `Character Movement`.

---

## 📍 PUNTO EXACTO EN EL QUE QUEDAMOS (Para retomar inmediatamente):

Hubo un error de runtime (`Accessed None` en `Get Enhanced Input Local Player Subsystem`) porque el registro de `IMC_Survival` estaba en el `BeginPlay` del Player Controller, momento en el cual el Local Player aún no está listo.

### Próxima acción a realizar:
1. En `GM_SurvivalPlayerControlle`: Asegurarse de que su `Event BeginPlay` esté desconectado/vacío.
2. En `BP_SurvivalCharacter`: En su `Event BeginPlay`, colocar:
   ```text
   [Event BeginPlay] ➔ [Cast To PlayerController] ➔ [Add Mapping Context (IMC_Survival)]
                              ▲                              ▲
                       [Get Controller]                      │
                              │                              │
                              └─➔ [Get Enhanced Input...]────┘
   ```
3. Compilar y darle a **Play** en el mapa para confirmar movimiento y zoom de apuntado fluido.

---

## 🎯 Siguientes Fases del Proyecto:
- **Fase 2: Sistema de Disparo y Daño**
  - Evento `IA_Shoot` (solo activo si `bIsAiming` es True).
  - Line Trace by Channel hacia el centro de la pantalla.
  - Efecto de impacto / retícula UMG / sonido de disparo.
- **Fase 3: Enemigo Básico con Behaviour Tree**
  - `BP_EnemyBase` con vida y lógica de daño por interfaz (`BPI_Damageable`).
  - Blackboard y Behavior Tree: Patrulla ➔ Persecución ➔ Ataque.
- **Fase 4: Interactuables y Recursos**
  - Pickup de munición / botiquín con `BPI_Interactable`.
  - Puerta con llave/mecanismo para cambiar de nivel.
- **Fase 5: Estructura de Niveles y UI**
  - Menú Principal, Menú de Pausa, Victoria / Game Over.
