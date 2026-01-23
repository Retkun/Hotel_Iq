import { NavItem } from './nav-item/nav-item';

export const navItems: NavItem[] = [
  {
    navCap: 'Acceuil',
  },
  {
    displayName: 'Dashboards Overview',
    iconName: 'solar:chart-square-line-duotone',
    route: '/kpi-overflow',
  },
  {
    displayName: 'Colt Dashboard',
    iconName: 'solar:widget-2-line-duotone',
    route: '/colt-dashboard',
  },
  {
    displayName: 'Webhelp Dashboard',
    iconName: 'solar:graph-line-duotone',
    route: '/webhelp-dashboard',
  },
  {
    displayName: 'Reservation Dashboard',
    iconName: 'solar:calendar-line-duotone',
    route: '/reservation-dashboard',
  },
  {
    displayName: 'Avis sur les Hotels',
    iconName: 'solar:star-line-duotone',
    route: '/hotels',
  },
];