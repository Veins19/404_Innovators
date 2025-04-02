-- Create tables
create table tasks (
    id bigint primary key generated always as identity,
    title text not null,
    description text,
    required_skills text[],
    required_people integer not null default 1,
    shift text not null check (shift in ('any', 'shift1', 'shift2')),
    status text not null default 'open' check (status in ('open', 'assigned')),
    assigned_to bigint[],
    created_at timestamp with time zone default timezone('utc'::text, now())
);

create table users (
    id bigint primary key generated always as identity,
    name text not null,
    skills text[] not null,
    availability text[] not null check (availability <@ array['shift1', 'shift2']),
    capacity integer not null check (capacity between 1 and 10)),
    current_tasks bigint[] default array[]::bigint[],
    created_at timestamp with time zone default timezone('utc'::text, now())
);

-- Enable RLS
alter table tasks enable row level security;
alter table users enable row level security;

-- Create policies
create policy "Public tasks access" on tasks
    for select using (true);

create policy "Public users access" on users
    for select using (true);