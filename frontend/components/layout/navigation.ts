import {
  History,
  LayoutDashboard,
  Settings,
  SquareCode,
  type LucideIcon,
} from "lucide-react";

export interface NavigationItem {
  label: string;
  href: string;
  icon: LucideIcon;
}

export const navigationItems: NavigationItem[] = [
  { label: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
  { label: "Workspace", href: "/workspace", icon: SquareCode },
  { label: "History", href: "/history", icon: History },
  { label: "Settings", href: "/settings", icon: Settings },
];
