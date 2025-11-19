# North Peru Foraging Hub Optimization

This repository documents a completed case study inspired by a large
cold–chain logistics network in Northern Peru.

The underlying system serves on the order of 10^5 points of sale across
multiple regions. Each point-of-sale represents a customer site with:

- Geographic coordinates (latitude, longitude)
- Average sales volume
- Number of refrigeration units and doors
- History of distribution and technical service visits
- Age of installed equipment

The study has two main objectives:

1. Identify **two strategic logistics centers** (warehouse + repair shop) for the Northern region, based on customer value and geography.
2. Analyse how different decision policies exploit this landscape of customers once the hubs are fixed, balancing travel effort and potential reward.

All code, anonymised data generation procedures and analyses are contained in this repository.

---

## 1. Customer dataset (~160k customers, anonymised)

The file `data/customers_synthetic_160k.csv` contains an **anonymised customer dataset** with approximately 160,000 rows spread across four regions.

The public dataset is not a direct extract of any operational database.  
Instead, it is built by fitting simple statistical models to internal aggregates
and sampling from those models. The goal is to preserve:

- the order of magnitude of the network,
- the joint behaviour of key variables (sales, equipment, services),
- and the broad spatial structure by region,

while ensuring that individual customers and exact locations cannot be recovered.

Each row represents a customer with the following key fields:

- `DSREG` – Region label (`NORTE`, `SUR`, `CENTRO`, `LIMA`)
- `CDCLIE` – Anonymised customer ID
- `NROPUESUM` – Total number of doors across all fridges at the location
- `VVENTASPROM` – Average sales volume (cases per period)
- `LATTUD`, `LNGTUD` – Latitude and longitude (randomised within regional envelopes)
- `CANTIDADEQ` – Number of refrigeration units installed
- `Cantserviciosdistri` – Number of distribution (truck) services
- `CantserviciosST` – Number of technical services
- `Cantidad_total_serv` – Total services (`Cantserviciosdistri + CantserviciosST`)

The generation process follows three principles:

1. **Preserve central behaviour**  
   For each region and variable, empirical distributions are approximated from
   internal data. Synthetic values are then drawn from smooth distributions
   centred on the bulk of the data. Extreme tails are truncated, which avoids
   creating artificial outliers and keeps most samples within a realistic
   “normal” range.

2. **Maintain relative scales**  
   Sales, number of units and service counts are generated on compatible scales,
   so that high–sales sites tend to have higher equipment counts and more
   service activity, as observed in real operations.

3. **Randomise locations while respecting geography**  
   Coordinates are sampled within plausible geographic envelopes for each
   region. This preserves the idea of dense and sparse areas while breaking
   any link to specific addresses.

A concise description of the fields and their construction is provided in
`data/README_data.md`. The notebook `notebooks/01_generate_synthetic_data.ipynb`
documents the anonymisation and sampling procedure in detail.

---

## 2. Customer importance and weighting scheme

Each customer is interpreted as a **patch** in a spatial landscape of demand
and maintenance effort. The study assigns an importance weight \(w_i\) to
customer \(i\) using three drivers:

- economic contribution (average sales),
- asset base (number of units to maintain),
- operational load (service history).

To make these components comparable, the raw variables are first **normalised**
within each region:

\[
\tilde{v}_i = \text{norm}(\text{VVENTASPROM}_i), \quad
\tilde{e}_i = \text{norm}(\text{CANTIDADEQ}_i), \quad
\tilde{s}_i = \text{norm}(\text{Cantidad\_total\_serv}_i),
\]

where `norm(·)` denotes a min–max rescaling that maps values to the interval
[0, 1] after trimming extreme tails. This step ensures that no component
dominates the weight purely due to units or raw magnitude.

The final weight is defined as:

\[
w_i = \alpha_v \tilde{v}_i +
      \alpha_e \tilde{e}_i +
      \alpha_s \tilde{s}_i,
\]

with coefficients:

- \(\alpha_v = 0.4\)  for sales,
- \(\alpha_e = 0.3\)  for installed units,
- \(\alpha_s = 0.3\)  for service activity.

### Why this weighting makes sense

The coefficients are chosen to reflect the joint priorities of a cold–chain
operation:

- Sales are given a slight advantage because they capture direct commercial
  impact and the potential benefit of protecting and developing a site.
- The number of units at a site concentrates asset risk: failures at a
  multi–unit site can affect a large volume of product and brand visibility.
- Service activity reflects actual field workload and the operational cost
  of keeping the site running.

A correlation analysis on the underlying system showed that these three
dimensions tend to move together at high–value locations. Using only one
indicator would miss important aspects of the network. The triplet
\((0.4, 0.3, 0.3)\) gives more influence to sales while keeping equipment
base and service history at comparable levels.

Several alternative triplets were tested. The ranking of high–weight customers
and the resulting hub locations remained stable under moderate changes of the
coefficients (perturbations up to ±0.1 in each weight). This robustness
suggests that the final choice is representative of a broader family of
reasonable trade–offs rather than a fragile tuning.

The complete computation and exploratory plots of the weights are contained in  
`notebooks/02_exploration_and_weights.ipynb`.

---

## 3. Two–hub optimisation for the Northern region

The central operational task is to position **two logistics centers** in the
Northern region that reflect both customer importance and travel effort.

The procedure implemented in `notebooks/03_weighted_hub_optimization.ipynb`
consists of:

1. Filtering customers with `DSREG == "NORTE"`.
2. Computing the importance weight \(w_i\) for each customer.
3. Applying a **weighted clustering algorithm** on the geographic coordinates
   (`LATTUD`, `LNGTUD`) with `k = 2`, using \(w_i\) as sample weights.
   K–Means from `scikit-learn` is used with fixed random seeds for
   reproducibility.
4. Interpreting the resulting cluster centres as **candidate hub locations**:
   - `Hub_1` = latitude/longitude of cluster centre 1,
   - `Hub_2` = latitude/longitude of cluster centre 2.
5. Computing geodesic distances from every customer to both hubs using the
   Haversine formula implemented in `src/geo_utils.py`.
6. Assigning each customer to the nearest hub and computing evaluation metrics:
   - weighted average distance,
   - distribution of total weight per hub,
   - coverage of the highest–weight customers.

Maps and summary tables in the notebook show how the two hubs partition the
Northern region and how well they cover the most relevant sites.

This approach replaces arbitrary hub placement with a transparent optimisation
based on customer value and spatial structure.

---

## 4. Decision policies on the hub–customer landscape

Once the two hubs are fixed, the repository analyses **decision policies**
that operate on the resulting landscape of weighted customers.

The notebook `notebooks/04_foraging_policies_simulation.ipynb` uses the
environment defined in `src/foraging_env.py` to simulate agents that:

- start from a selected hub,
- have a limited travel budget,
- choose a sequence of customers to visit in order to maximise collected reward.

The implementation compares policies such as:

- a distance–based heuristic that always visits the nearest unserved customer,
- a weight–based heuristic that prioritises sites with higher \(w_i\),
- an exploratory policy that balances distance and weight through a simple
  learning rule over repeated visits.

For each policy, the notebook reports:

- total collected reward,
- total travel distance,
- distribution of visits across customers,
- qualitative differences in which areas are favoured or neglected.

These simulations illustrate how the same hub configuration can lead to
different utilisation patterns depending on the decision mechanism driving
field operations. They also provide a bridge between static hub design and
dynamic decision behaviour over time.

---

## 5. Repository structure

```text
north-peru-foraging-hub-optimization/
│
├─ README.md
├─ data/
│   ├─ customers_synthetic_160k.csv
│   └─ README_data.md
├─ notebooks/
│   ├─ 01_generate_synthetic_data.ipynb
│   ├─ 02_exploration_and_weights.ipynb
│   ├─ 03_weighted_hub_optimization.ipynb
│   └─ 04_foraging_policies_simulation.ipynb
└─ src/
    ├─ __init__.py
    ├─ geo_utils.py
    └─ foraging_env.py
```
01_generate_synthetic_data.ipynb
Documents the construction of the anonymised dataset from regional
aggregates and fitted distributions.

02_exploration_and_weights.ipynb
Performs exploratory analysis and computes customer importance weights.

03_weighted_hub_optimization.ipynb
Executes the weighted clustering procedure and evaluates the two selected hubs.

04_foraging_policies_simulation.ipynb
Simulates decision policies on top of the optimised hub–customer landscape.


### 6. Requirements

Main dependencies:

Python 3.10+

pandas

numpy

scikit-learn

matplotlib

jupyter or jupyterlab

The repository is self–contained and can be reproduced by installing the
listed packages and running the notebooks in numerical order.
