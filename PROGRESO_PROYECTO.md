# Documentación de Traspaso y Estado del Proyecto — Survival Horror RE4 (UADE)

> **Propósito de este documento**: Este archivo resume toda la consigna universitaria, la arquitectura técnica actual del proyecto en Unreal Engine 5.3 (`TpUnreal`) y los pasos exactos pendientes para continuar el desarrollo en otra computadora sin perder contexto.

---

## 1. Contexto Académico y Consigna (UADE - Desarrollo Avanzado de Videojuegos)

El trabajo práctico consiste en desarrollar un **videojuego 3D jugable en Unreal Engine** (género elegido: **Survival Horror con cámara al hombro estilo Resident Evil 4**).

### Requisitos Obligatorios de la Cátedra:
1. **No copiar/pegar el Template como base**: Toda la lógica debe vivir en nuestra propia arquitectura (`Content/SurvivalHorror/`) haciendo uso correcto del **Gameplay Framework** (`GameMode`, `PlayerController`, `Character`).
2. **Estructura de la Experiencia (Gameloop completo)**:
   - Menú Principal (inicio de partida).
   - Al menos **2 niveles de gameplay** con progresión entre ambos (el 2do de mayor exigencia) + **Zona Segura inicial**.
   - **Pausa funcional** durante el gameplay.
   - **Pantalla de Victoria y Pantalla de Derrota**.
3. **Jugador (Enhanced Input, Animación y UI)**:
   - Uso obligatorio de `Enhanced Input` (`IMC_Survival` + `Input Actions`).
   - Animation Blueprint con State Machine.
   - Interfaz UMG (`WBP_HUD`) que refleje los estados del jugador (vida, estado FINE/CAUTION/DANGER, munición `Cargador / Inventario`, mira y objetivo).
4. **Desafío (IA con Behavior Tree)**:
   - Enemigos controlados por IA mediante `AIController`, `Blackboard`, `Behavior Tree` y `AI Perception`.
5. **Interacciones con el Mundo (Mínimo 2 sistemas)**:
   - Implementado mediante **Blueprint Interface** (`BPI_Interactable`) para recolectar recursos (Munición, Botiquín, Llaves) y abrir puertas de progresión/victoria.
6. **Criterios de Evaluación (10 puntos)**:
   - Gameplay Framework y Gameloop: **3,0 pts**
   - Mecánicas, interacción y desafío: **2,0 pts**
   - UI y comunicación al jugador: **1,5 pts**
   - Estructura del proyecto y buenas prácticas (Interfaces, Event Dispatchers, orden): **1,5 pts**
   - Pulido audiovisual (Sonidos, VFX, Materiales, Animaciones): **1,0 pt**
   - Herramientas avanzadas de Unreal (Behavior Tree, AI Perception, etc.): **1,0 pt**
7. **Entregables Finales**:
   - Documento PDF (`TP_NombreDelGrupo.pdf` con: Título, Descripción/Referencias, Actores, Mecánicas, Metas y obstáculos, Reglas, Espacio).
   - Proyecto de Unreal Engine (Repositorio / ZIP que compile sin errores).
   - Build ejecutable del juego en ZIP (sin crasheos en el flujo principal).

---

## 2. Estado Actual del Proyecto (Qué YA está implementado y funcionando)

Todo nuestro contenido propio se encuentra en `Content/SurvivalHorror/`:

### A. Core y Gameplay Framework (`Content/SurvivalHorror/Blueprints/Core/`)
- **`GM_SurvivalGameMode.uasset`**: Configurado con `BP_SurvivalCharacter` como Default Pawn y `GM_SurvivalPlayerControlle` como Player Controller.
- **`GM_SurvivalPlayerControlle.uasset`**: Controlador propio del jugador.

### B. Personaje Principal (`Content/SurvivalHorror/Blueprints/Characters/BP_SurvivalCharacter.uasset`)
- **Movimiento y Cámara RE4**:
  - `CameraBoom` (SpringArm) con Socket Offset lateral al hombro derecho y Camera Lag.
  - Giro natural hacia el movimiento (`Orient Rotation to Movement = True`) al caminar normal, y alineación con la mira (`Use Controller Rotation Yaw = True` + velocidad reducida a `200`) al apuntar.
  - **Apuntado (`IA_Aim` + `TL_Aim`)**: Zoom suave interpolando el FOV de `90` a `65` con Timeline y mostrando/ocultando la mira en el HUD.
- **Combate y Sistema de Recarga estilo Resident Evil (`IA_Shoot` + `IA_Reload`)**:
  - Variables:
    - `Ammo` (Int): Balas dentro del cargador del arma (máximo **12**).
    - `MaxAmmo` (Int): Balas acumulables en el inventario/reserva.
    - `BulletsToRecharge` (Int): Variable auxiliar que calcula `Min(12 - Ammo, MaxAmmo)` al presionar **`R` (`IA_Reload`)** para transferir balas del inventario al cargador y actualizar el HUD mediante `OnAmmoChanged`.
  - Disparo mediante `LineTraceByChannel` desde `FollowCamera`, aplicando daño con `ApplyDamage`.
- **Salud y Muerte (`Event AnyDamage`)**:
  - Variables: `Health` (`100.0`), `MaxHealth` (`100.0`), `bIsDead` (Bool).
  - Event Dispatchers: **`OnHealthChanged`** y **`OnAmmoChanged`** (conectados al HUD).
  - Al llegar `Health <= 0`: activa física **Ragdoll**, desactiva input/movimiento, espera `2.0` segundos (`Delay`) y muestra **`WBP_GameOver`** habilitando el cursor en modo `UI Only`.
- **Interacción desde la Mira (`IA_Interact` - Tecla E)**:
  - Lanza un `SphereTraceByChannel` (`Radius = 25`, distancia `500`) desde el centro de `FollowCamera` hacia adelante y envía el mensaje **`Interact`** de la interfaz **`BPI_Interactable`**.
  - Variable **`bHasKey`** (Bool) para registrar si el jugador recogió la llave del nivel.

### C. Inteligencia Artificial de Enemigos (`Content/SurvivalHorror/Blueprints/Enemies/`)
- **`BP_Zombie.uasset`**: Recibe daño (`Event AnyDamage`), descuenta vida y entra en estado **Ragdoll** al morir.
- **`AIC_Zombie.uasset`**: Usa **`AIPerceptionComponent`** (vista con `SightRadius` y `LoseSightRadius`) para detectar al jugador y actualizar `TargetActor` en el Blackboard.
- **`BB_Zombie.uasset` y `BT_Zombie.uasset`**: Blackboard y Behavior Tree completos con patrullaje (**`BTT_FindPatrolPoint`**), persecución y ataque cuerpo a cuerpo (**`BTT_ZombieAttack`** que aplica daño al jugador).

### D. Objetos Interactuables del Mundo (`Content/SurvivalHorror/Blueprints/Items/`)
Todos implementan la interfaz **`BPI_Interactable`** (`Content/SurvivalHorror/UI/BPI_Interactable.uasset`):
- **`BP_AmmoPickup.uasset`**: Suma `+5` balas a la reserva de inventario (`MaxAmmo`), llama a `OnAmmoChanged` y se destruye.
- **`BP_MedkitPickup.uasset`**: Cura `+35` de vida (`Health`) con `Clamp(0, MaxHealth)`, llama a `OnHealthChanged` y se destruye (con colisión simplificada aplicada al Static Mesh `medkit_son`).
- **`BP_KeyPickup.uasset`**: Activa `bHasKey = True` en el personaje y se destruye.
- **`BP_LockedDoor.uasset` / `BP_LockedDoor1.uasset` / `BP_LockedWinnerDoor.uasset`**: Verifica `bHasKey`; si no tiene la llave avisa en pantalla, y si la tiene permite avanzar de nivel o dispara la pantalla **`WBP_Victory`**.

### E. Interfaz de Usuario (`Content/SurvivalHorror/UI/`)
- **`WBP_HUD.uasset`**: Barra de vida, estado estilo RE (`FINE` / `CAUTION` / `DANGER`), contador de munición (`Ammo / MaxAmmo`), mira central y texto de objetivo.
- **`WBP_GameOver.uasset`**: Pantalla de derrota ("HAS MUERTO") con botón **Reintentar** (recarga el nivel actual y devuelve el control `Game Only`) y botón **Salir**.
- **`WBP_Victory.uasset`**: Pantalla de victoria ("¡SOBREVIVISTE!") al escapar por la puerta final.

---

## 3. Qué Falta Implementar (Próximos Pasos Exactos)

### Paso Pendiente 1: Menú de Pausa (`WBP_PauseMenu` + `IA_Pause`)
1. Duplicar `WBP_GameOver` en `Content/SurvivalHorror/UI/` y nombrarlo **`WBP_PauseMenu`**.
2. Cambiar el título a **"PAUSA"** y el botón superior a **"Continuar"**.
3. En el `On Clicked` del botón Continuar: llamar a `Set Game Paused (False)`, `Set Input Mode Game Only`, `Set Show Mouse Cursor (False)` y `Remove from Parent`.
4. Crear `IA_Pause` en `Content/SurvivalHorror/Input/Actions/`, asignarlo a la tecla **`P`** o **`Tab`** en `IMC_Survival`, y en `BP_SurvivalCharacter` crear el widget `WBP_PauseMenu` y llamar a `Set Game Paused (True)`.

### Paso Pendiente 2: Menú Principal (`WBP_MainMenu` + Mapa `Lvl_MainMenu`)
1. Duplicar `WBP_GameOver` y nombrarlo **`WBP_MainMenu`**.
2. Cambiar el botón principal a **"Jugar"** para que ejecute `Open Level (by Name)` hacia el Nivel 1.
3. Crear el mapa vacío `Content/SurvivalHorror/Maps/Lvl_MainMenu.umap` y en su *Level Blueprint* (`Event BeginPlay`) mostrar `WBP_MainMenu` en viewport con el ratón activo.

### Paso Pendiente 3: Armado de los 2 Niveles Jugables (`Lvl_01` y `Lvl_02`)
1. **Nivel 1 (`Lvl_01_SafeZone`)**: Sala inicial segura con cajas de munición y botiquín + pasillo con los primeros zombies + llave + `BP_LockedDoor` que hace `Open Level` hacia el Nivel 2.
2. **Nivel 2 (`Lvl_02_Survival`)**: Escenario más exigente con más zombies, menos recursos, llave final y `BP_LockedWinnerDoor` que muestra `WBP_Victory`.

### Paso Pendiente 4: Pulido Audiovisual (1,0 pt de la rúbrica)
1. Agregar un componente **`SpotLight`** (Linterna) dentro de `FollowCamera` o `Mesh` en `BP_SurvivalCharacter` que se encienda/apague con la tecla **`F`**.
2. Agregar nodos `Play Sound at Location` / `Play Sound 2D` al disparar, recargar, recoger ítems y recibir daño.
