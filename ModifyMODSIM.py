def update_xy_timeseries(xy_path, df, scenario_name):
    """
    Updates inflow and demand node time series in a MODSIM .xy file.
    - Inflow nodes use 'tsinflow' and are bounded by 'units' to 'pos'
    - Demand nodes end in '_LD' and are bounded by 'units' to 'node'
    If structure is not found, the node is skipped with a warning.
    """
    with open(xy_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    updated_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]

        # Look for node start
        if line.strip().startswith("name "):
            node_name = line.strip().split(" ", 1)[1]

            if node_name in df.columns:
                is_demand = node_name.endswith("_LD")
                end_tag = "node" if is_demand else "pos"

                # Capture block from this node to end_tag
                block_start = i
                found_units = False
                found_endtag = False
                unit_index = -1
                end_index = -1

                # Scan forward to find 'units' and end tag (pos or node)
                j = i
                while j < len(lines):
                    l = lines[j]
                    if l.strip().startswith("units"):
                        unit_index = j
                        found_units = True
                    if l.strip() == end_tag:
                        end_index = j
                        found_endtag = True
                        break
                    j += 1

                if not found_units or not found_endtag or unit_index >= end_index:
                    print(f"⚠️ Skipping {node_name}: required structure not found (units and {end_tag})")
                    updated_lines.append(line)
                    i += 1
                    continue

                # Keep lines up to 'units'
                updated_lines.extend(lines[block_start:unit_index])
                updated_lines.append("units 1000 m³/day\n")

                # Add time series
                for date, value in zip(df["Date"], df[node_name]):
                    updated_lines.append(f"{date}\t{value}\n")

                # Reinsert end tag (pos/node) and continue from after end tag
                updated_lines.append(f"{end_tag}\n")
                i = end_index + 1
                continue

        # Default case — copy line
        updated_lines.append(line)
        i += 1

    # Save result
    with open(xy_path, 'w', encoding='utf-8') as f:
        f.writelines(updated_lines)

    #print(f"✅ Time series updated for {scenario_name}")