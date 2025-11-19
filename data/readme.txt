
# Dataset documentation — Synthetic customer data (Northern Peru)

This folder contains the anonymised datasets used throughout the
*North Peru Foraging Hub Optimization* study.

The data provided here **does not contain any real operational records**.
All customer information has been fully reconstructed using fitted
statistical distributions and regional geographic envelopes.  
The goal is to preserve the *structure* of a large cold–chain network
without exposing identifiable business information.

---

## Files included

### 1. `customers_synthetic_160k.csv`
A synthetic dataset representing ~160,000 customer locations across the
four major regions of Peru.  
This file simulates the full customer network and is used as the
starting point for exploratory analysis and importance weighting.

Each generated row contains:

- **DSREG** — Region (`NORTE`, `SUR`, `CENTRO`, `LIMA`)  
- **CDCLIE** — Anonymised customer ID  
- **NROPUESUM** — Total number of cooler doors  
- **VVENTASPROM** — Average sales volume  
- **LATTUD**, **LNGTUD** — Randomised coordinates within regional bounds  
- **CANTIDADEQ** — Number of refrigeration units  
- **EDADDIAS** — Age of equipment (days)  
- **Cantserviciosdistri** — Number of distribution services  
- **CantserviciosST** — Number of technical services  
- **Cantidad_total_serv** — Total service interventions  
- **TIEMPO DE EJECUCION PROMEDIO (MINUTOS)** — Average service duration  
- **TIEMPO PROMEDIO DE LLAMADOS (DIAS)** — Average response time  
- **DEPARTAMENTO** — High-level administrative division (synthetic)

These variables were generated using simple probabilistic models to match
the central tendencies of real-world operational data while preventing
any possibility of reverse engineering.

---

### 2. `customers_synthetic_north.csv`
A filtered extract of the synthetic dataset containing only customers
from the **Northern region**.  
This file is the primary input for:

- the **importance weighting**,
- the **two–hub optimisation**, and
- the **decision policy simulations**.

It preserves the statistical structure of the full dataset but reduces
the scope to the region of interest for the case study.

---

## Notes on anonymisation

- **Coordinates** are jittered and reshaped within broad regional envelopes.  
  No point corresponds to a real address or business location.

- **IDs** (CDCLIE) are randomised hashes with no mapping to internal
  systems.

- **Operational variables** (sales, services, equipment counts) are
  sampled from fitted distributions using trimmed ranges to prevent
  artificial outliers.

- **Derived fields** used later in the project (hub assignment,
  distance to hubs, optimal zones, etc.) are **not** included here to
  ensure the dataset remains purely “pre-analysis”.

---

## Usage

These files are read directly by the Jupyter notebooks in the
`notebooks/` folder.  
If you want to regenerate the synthetic dataset from scratch, refer to:

notebooks/01_generate_synthetic_data.ipynb



For reproducibility, all fixed seeds, regional envelopes and sampling
steps are fully documented in that notebook.

---

## File size considerations

The 160k synthetic dataset is moderately large.  
If GitHub storage limits require it, consider compressing the CSV or
storing it via Git LFS.  
The Northern subset is much lighter and always fits within normal limits.

---

If additional synthetic variables or region-specific subsets are needed,
they can be safely added to this folder following the same structure and
anonymisation rules.


