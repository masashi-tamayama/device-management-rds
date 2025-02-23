export interface Device {
    id: string;
    name: string;
    manufacturer: string;
    created_at: string;
    updated_at: string;
}

export interface DeviceCreateInput {
    name: string;
    manufacturer: string;
}

export interface DeviceUpdateInput {
    name: string;
    manufacturer: string;
} 